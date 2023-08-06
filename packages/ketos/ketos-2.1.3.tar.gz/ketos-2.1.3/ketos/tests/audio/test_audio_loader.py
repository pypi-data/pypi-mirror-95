# ================================================================================ #
#   Authors: Fabio Frazao and Oliver Kirsebom                                      #
#   Contact: fsfrazao@dal.ca, oliver.kirsebom@dal.ca                               #
#   Organization: MERIDIAN (https://meridian.cs.dal.ca/)                           #
#   Team: Data Analytics                                                           #
#   Project: ketos                                                                 #
#   Project goal: The ketos library provides functionalities for handling          #
#   and processing acoustic data and applying deep neural networks to sound        #
#   detection and classification tasks.                                            #
#                                                                                  #
#   License: GNU GPLv3                                                             #
#                                                                                  #
#       This program is free software: you can redistribute it and/or modify       #
#       it under the terms of the GNU General Public License as published by       #
#       the Free Software Foundation, either version 3 of the License, or          #
#       (at your option) any later version.                                        #
#                                                                                  #
#       This program is distributed in the hope that it will be useful,            #
#       but WITHOUT ANY WARRANTY; without even the implied warranty of             #
#       MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the              #
#       GNU General Public License for more details.                               # 
#                                                                                  #
#       You should have received a copy of the GNU General Public License          #
#       along with this program.  If not, see <https://www.gnu.org/licenses/>.     #
# ================================================================================ #

""" Unit tests for the 'audio.audio_loader' module within the ketos library
"""
import pytest
import json
import os
import numpy as np
import pandas as pd
from io import StringIO
from ketos.audio.waveform import Waveform
from ketos.audio.spectrogram import MagSpectrogram
from ketos.audio.audio_loader import AudioFrameLoader, AudioSelectionLoader
from ketos.data_handling.selection_table import use_multi_indexing, standardize
from ketos.data_handling.data_handling import find_wave_files
from ketos.data_handling.parsing import parse_audio_representation
from ketos.audio.utils.misc import from_decibel

current_dir = os.path.dirname(os.path.realpath(__file__))
path_to_assets = os.path.join(os.path.dirname(current_dir),"assets")

def test_init_audio_frame_loader_with_folder(five_time_stamped_wave_files):
    """ Test that we can initialize an instance of the AudioFrameLoader class from a folder"""
    loader = AudioFrameLoader(path=five_time_stamped_wave_files, frame=0.5)
    assert len(loader.sel_gen.files) == 5

def test_init_audio_frame_loader_with_wav_file(sine_wave_file):
    """ Test that we can initialize an instance of the AudioFrameLoader class 
        from a single wav file"""
    loader = AudioFrameLoader(filename=sine_wave_file, frame=0.5)
    assert len(loader.sel_gen.files) == 1
    assert loader.num() == 6

def test_init_audio_frame_loader_with_batches(sine_wave_file):
    """ Test that we can initialize an instance of the AudioFrameLoader class 
        from a single wav file with a batch size greater than 1"""
    loader = AudioFrameLoader(filename=sine_wave_file, frame=0.5, batch_size=2)
    assert len(loader.sel_gen.files) == 1
    assert loader.num() == 6

def test_init_audio_frame_loader_with_batch_size_one_file(sine_wave_file):
    """ Test that we can initialize an instance of the AudioFrameLoader class 
        from a single wav file with a batch size equal to 1 file"""
    loader = AudioFrameLoader(filename=sine_wave_file, frame=0.5, batch_size='FILE')
    assert len(loader.sel_gen.files) == 1
    assert loader.num() == 6

def test_audio_frame_loader_gives_same_output_with_batches(sine_wave_file):
    """ Test that segments returned by the AudioFrameLoader class are independent of batch size"""
    rep = {'type':'MagSpectrogram','window':0.1,'step':0.02,'freq_max':800}
    fname = os.path.join(path_to_assets, 'grunt1.wav')
    loader1 = AudioFrameLoader(filename=fname, frame=0.4, step=0.12, repres=rep, batch_size=1)
    loader3 = AudioFrameLoader(filename=fname, frame=0.4, step=0.12, repres=rep, batch_size=3)
    loaderf = AudioFrameLoader(filename=fname, frame=0.4, step=0.12, repres=rep, batch_size='file')
    for i in range(loader1.num()):
        x1 = next(loader1)
        x3 = next(loader3)
        xf = next(loaderf)
        dx = x1.data - x3.data
        assert np.mean(np.abs(dx)) < 0.1
        dx = x1.data - xf.data
        assert np.mean(np.abs(dx)) < 0.1

def test_audio_frame_loader_mag(five_time_stamped_wave_files):
    """ Test that we can use the AudioFrameLoader class to compute MagSpectrograms""" 
    rep = {'type':'MagSpectrogram','window':0.1,'step':0.02}
    loader = AudioFrameLoader(path=five_time_stamped_wave_files, frame=0.5, repres=rep)
    assert len(loader.sel_gen.files) == 5
    assert loader.num() == 5
    s = next(loader)
    assert s.duration() == 0.5
    s = next(loader)
    assert s.duration() == 0.5
    assert loader.sel_gen.file_id == 2
    loader.reset()
    assert loader.sel_gen.file_id == 0

def test_audio_frame_loader_multiple_representations(five_time_stamped_wave_files):
    """ Test that we can use the AudioFrameLoader class to load multiple audio representations""" 
    rep1 = {'type':'Waveform'}
    rep2 = {'type':'MagSpectrogram','window':0.1,'step':0.02}
    loader = AudioFrameLoader(path=five_time_stamped_wave_files, frame=0.5, repres=[rep1, rep2])
    assert len(loader.sel_gen.files) == 5
    assert loader.num() == 5
    s = next(loader)
    assert len(s) == 2
    assert type(s[0]) == Waveform
    assert type(s[1]) == MagSpectrogram
    assert s[0].duration() == 0.5
    s = next(loader)
    assert s[1].duration() == 0.5
    assert loader.sel_gen.file_id == 2
    loader.reset()
    assert loader.sel_gen.file_id == 0

def test_audio_frame_loader_mag_in_batches(five_time_stamped_wave_files):
    """ Test that we can use the AudioFrameLoader class to compute MagSpectrograms 
        in batches""" 
    rep = {'type':'MagSpectrogram','window':0.1,'step':0.02}
    loader = AudioFrameLoader(path=five_time_stamped_wave_files, frame=0.26, repres=rep, batch_size=3)
    assert len(loader.sel_gen.files) == 5
    assert loader.num() == 10
    s = next(loader) 
    assert loader.sel_gen.file_id == 1
    assert s.duration() == 0.26
    assert s.offset == 0
    s = next(loader)
    assert loader.sel_gen.file_id == 1
    assert s.duration() == 0.26
    assert s.offset == 0.26
    s = next(loader)
    assert loader.sel_gen.file_id == 2
    assert s.duration() == 0.26
    assert s.offset == 0

def test_audio_frame_loader_mag_in_batches_1_file(five_time_stamped_wave_files):
    """ Test that we can use the AudioFrameLoader class to compute MagSpectrograms 
        in batches of 1 file per batch""" 
    rep = {'type':'MagSpectrogram','window':0.1,'step':0.02}
    loader = AudioFrameLoader(path=five_time_stamped_wave_files, frame=0.12, repres=rep, batch_size='file')
    assert len(loader.sel_gen.files) == 5
    assert loader.num() == 25
    assert loader.sel_gen.file_id == 1
    s = next(loader) 
    assert loader.sel_gen.file_id == 1
    assert s.duration() == 0.12
    assert s.offset == 0
    s = next(loader)
    assert loader.sel_gen.file_id == 1
    assert s.duration() == 0.12
    assert s.offset == 0.12
    s = next(loader)
    s = next(loader)
    s = next(loader)
    assert loader.sel_gen.file_id == 1
    s = next(loader)
    assert loader.sel_gen.file_id == 2

def test_audio_frame_loader_norm_mag(sine_wave_file):
    """ Test that we can initialize the AudioFrameLoader class to compute MagSpectrograms
        with the normalize_wav option set to True""" 
    rep = {'type':'MagSpectrogram','window':0.1,'step':0.02}
    loader = AudioFrameLoader(filename=sine_wave_file, frame=0.5, repres=rep)
    spec1 = next(loader)
    spec1 = next(loader)
    rep = {'type':'MagSpectrogram','window':0.1,'step':0.02, 'normalize_wav': True}
    loader = AudioFrameLoader(filename=sine_wave_file, frame=0.5, repres=rep)
    spec2 = next(loader)
    spec2 = next(loader)
    d1 = from_decibel(spec1.get_data())
    d2 = from_decibel(spec2.get_data()) / np.sqrt(2)
    assert np.all(np.isclose(np.mean(d1), np.mean(d2), rtol=2e-2))

def test_audio_frame_loader_mag_transforms(sine_wave_file):
    """ Test that we can initialize the AudioFrameLoader class to compute MagSpectrograms
        with various transformations applied""" 
    range_trans = {'name':'adjust_range', 'range':(0,1)}
    enh_trans = {'name':'enhance_signal','enhancement':2.3}
    transforms = [range_trans, enh_trans]
    norm_trans = {'name':'normalize','mean':0.5,'std':2.0}
    noise_trans = {'name':'add_gaussian_noise', 'sigma':2.0}
    wf_transforms = [norm_trans, noise_trans]
    rep = {'type':'MagSpectrogram','window':0.1,'step':0.02, 'transforms':transforms, 'waveform_transforms':wf_transforms}
    loader = AudioFrameLoader(filename=sine_wave_file, frame=0.5, repres=rep)
    spec1 = next(loader)
    assert spec1.transform_log == transforms
    assert spec1.waveform_transform_log == wf_transforms

def test_audio_frame_loader_dur(five_time_stamped_wave_files):
    """ Test that we can use the AudioFrameLoader class to compute MagSpectrograms
        with durations shorter than file durations""" 
    rep = {'type':'MagSpectrogram','window':0.1,'step':0.02}
    loader = AudioFrameLoader(path=five_time_stamped_wave_files, frame=0.2, repres=rep)
    assert len(loader.sel_gen.files) == 5
    s = next(loader)
    assert s.duration() == 0.2
    s = next(loader)
    assert s.duration() == 0.2
    s = next(loader)
    assert s.duration() == 0.2
    assert loader.sel_gen.file_id == 1

def test_audio_frame_loader_frame_None(five_time_stamped_wave_files):
    """ Test that we can use the AudioFrameLoader class to compute MagSpectrograms
        without specifying the frame argument""" 
    rep = {'type':'MagSpectrogram','window':0.1,'step':0.02,'duration':0.2}
    loader = AudioFrameLoader(path=five_time_stamped_wave_files, repres=rep)
    assert len(loader.sel_gen.files) == 5
    s = next(loader)
    assert s.duration() == 0.2
    s = next(loader)
    assert s.duration() == 0.2
    s = next(loader)
    assert s.duration() == 0.2
    assert loader.sel_gen.file_id == 1

def test_audio_frame_loader_overlap(five_time_stamped_wave_files):
    """ Test that we can use the AudioFrameLoader class to compute overlapping 
        MagSpectrograms""" 
    rep = {'type':'MagSpectrogram','window':0.1,'step':0.02}
    loader = AudioFrameLoader(path=five_time_stamped_wave_files, frame=0.2, step=0.06, repres=rep)
    assert len(loader.sel_gen.files) == 5
    s = next(loader)
    assert s.duration() == 0.2
    s = next(loader)
    assert s.duration() == 0.2
    s = next(loader)
    assert s.duration() == 0.2
    assert loader.sel_gen.time == pytest.approx(3*0.06, abs=1e-6)
    assert loader.sel_gen.file_id == 0

def test_audio_frame_loader_overlap_batches(five_time_stamped_wave_files):
    """ Test that we can use the AudioFrameLoader class to compute overlapping 
        MagSpectrograms in batches""" 
    rep = {'type':'MagSpectrogram','window':0.1,'step':0.02}
    loader = AudioFrameLoader(path=five_time_stamped_wave_files, frame=0.2, step=0.06, repres=rep, batch_size=2)
    assert len(loader.sel_gen.files) == 5
    s = next(loader)
    assert s.duration() == 0.2
    s = next(loader)
    assert s.duration() == 0.2
    s = next(loader)
    assert s.duration() == 0.2
    assert loader.sel_gen.time == pytest.approx(5*0.06, abs=1e-6)
    assert loader.sel_gen.file_id == 0

def test_audio_frame_loader_uniform_length(five_time_stamped_wave_files):
    """ Check that the AudioFrameLoader always returns segments of the same length""" 
    rep = {'type':'MagSpectrogram','window':0.1,'step':0.02}
    loader = AudioFrameLoader(path=five_time_stamped_wave_files, frame=0.2, repres=rep)
    assert len(loader.sel_gen.files) == 5
    for _ in range(10):
        s = next(loader)
        assert s.duration() == 0.2

def test_audio_frame_loader_number_of_segments(sine_wave_file):
    """ Check that the AudioFrameLoader computes expected number of segments""" 
    rep = {'type':'MagSpectrogram','window':0.1,'step':0.01,'rate':2341}
    import librosa
    dur = librosa.core.get_duration(filename=sine_wave_file)
    # duration is an integer number of lengths
    l = 0.2
    loader = AudioFrameLoader(filename=sine_wave_file, frame=l, repres=rep)
    assert len(loader.sel_gen.files) == 1
    N = int(dur / l)
    assert N == loader.sel_gen.num_segs[0]
    # duration is *not* an integer number of lengths
    l = 0.21
    loader = AudioFrameLoader(filename=sine_wave_file, frame=l, repres=rep)
    N = int(np.ceil(dur / l))
    assert N == loader.sel_gen.num_segs[0]
    # loop over all segments
    for _ in range(N):
        _ = next(loader)
    # non-zero overlap
    l = 0.21
    o = 0.8*l
    loader = AudioFrameLoader(filename=sine_wave_file, frame=l, step=l-o, repres=rep)
    step = l - o
    N = int(np.ceil((dur-l) / step) + 1)
    assert N == loader.sel_gen.num_segs[0]
    # loop over all segments
    for _ in range(N):
        _ = next(loader)

def test_audio_select_loader_mag(five_time_stamped_wave_files):
    """ Test that we can use the AudioSelectionLoader class to compute MagSpectrograms""" 
    rep = {'type':'MagSpectrogram','window':0.1,'step':0.02}
    # create a selection table
    files = find_wave_files(path=five_time_stamped_wave_files, return_path=False, search_subdirs=True)
    sel = pd.DataFrame({'filename':[files[0],files[1]],'start':[0.10,0.12],'end':[0.46,0.42]})
    sel = use_multi_indexing(sel, 'sel_id')
    # init loader
    loader = AudioSelectionLoader(path=five_time_stamped_wave_files, selections=sel, repres=rep)
    assert loader.num() == 2
    s = next(loader)
    assert s.duration() == pytest.approx(0.36, abs=1e-6)
    s = next(loader)
    assert s.duration() == pytest.approx(0.30, abs=1e-6)

def test_audio_select_loader_with_labels(five_time_stamped_wave_files):
    """ Test that we can use the AudioSelectionLoader class to compute MagSpectrograms with labels""" 
    rep = {'type':'MagSpectrogram','window':0.1,'step':0.02}
    # create a selection table
    files = find_wave_files(path=five_time_stamped_wave_files, return_path=False, search_subdirs=True)
    sel = pd.DataFrame({'filename':[files[0],files[1]],'start':[0.10,0.12],'end':[0.46,0.42],'label':[3,5]})
    sel = use_multi_indexing(sel, 'sel_id')
    # init loader
    loader = AudioSelectionLoader(path=five_time_stamped_wave_files, selections=sel, repres=rep)
    s = next(loader)
    assert s.duration() == pytest.approx(0.36, abs=1e-6)
    assert s.label == 3
    s = next(loader)
    assert s.duration() == pytest.approx(0.30, abs=1e-6)
    assert s.label == 5

def test_audio_select_loader_with_annots(five_time_stamped_wave_files):
    """ Test that we can use the AudioSelectionLoader class to compute MagSpectrograms
        while including annotation data""" 
    rep = {'type':'MagSpectrogram','window':0.1,'step':0.02}
    files = find_wave_files(path=five_time_stamped_wave_files, return_path=False, search_subdirs=True)
    # create a selection table
    sel = pd.DataFrame({'filename':[files[0],files[1]],'start':[0.10,0.12],'end':[0.46,0.42]})
    sel = use_multi_indexing(sel, 'sel_id')
    # create a annotation table
    ann = pd.DataFrame({'filename':[files[0],files[0],files[1]],'label':[3,5,4],'start':[0.05,0.06,0.20],'end':[0.30,0.16,0.60]})
    ann = standardize(ann)
    # init loader
    loader = AudioSelectionLoader(path=five_time_stamped_wave_files, selections=sel, annotations=ann, repres=rep)
    s = next(loader)
    assert s.duration() == pytest.approx(0.36, abs=1e-6)
    d = '''label  start   end  freq_min  freq_max
0      1    0.0  0.20       NaN       NaN
1      3    0.0  0.06       NaN       NaN'''
    ans = pd.read_csv(StringIO(d), delim_whitespace=True, index_col=[0,1])
    res = s.get_annotations()[ans.columns.values]
    pd.testing.assert_frame_equal(ans, res)
    s = next(loader)
    assert s.duration() == pytest.approx(0.30, abs=1e-6)
    d = '''label  start  end  freq_min  freq_max
0      2   0.08  0.3       NaN       NaN'''
    ans = pd.read_csv(StringIO(d), delim_whitespace=True, index_col=[0,1])
    res = s.get_annotations()[ans.columns.values]
    pd.testing.assert_frame_equal(ans, res)

def test_audio_frame_loader_mag_json(five_time_stamped_wave_files, spectr_settings):
    """ Test that we can use the AudioFrameLoader class to compute MagSpectrograms from json settings""" 
    data = json.loads(spectr_settings)
    rep = parse_audio_representation(data['spectrogram'])
    loader = AudioFrameLoader(path=five_time_stamped_wave_files, frame=0.5, repres=rep)
    assert len(loader.sel_gen.files) == 5
    s = next(loader)
    assert s.duration() == 0.5
    s = next(loader)
    assert s.duration() == 0.5
    assert loader.sel_gen.file_id == 2

def test_audio_frame_loader_accepts_filename_list(five_time_stamped_wave_files, spectr_settings):
    """ Test that we can use the AudioFrameLoader class to compute MagSpectrograms from json settings""" 
    data = json.loads(spectr_settings)
    rep = parse_audio_representation(data['spectrogram'])
    filename = ['empty_HMS_12_ 5_ 0__DMY_23_ 2_84.wav', 
                'empty_HMS_12_ 5_ 1__DMY_23_ 2_84.wav',
                'empty_HMS_12_ 5_ 2__DMY_23_ 2_84.wav']
    loader = AudioFrameLoader(path=five_time_stamped_wave_files, filename=filename, frame=0.5, repres=rep)
    assert len(loader.sel_gen.files) == 3
    s = next(loader)
    assert s.duration() == 0.5
    s = next(loader)
    assert s.duration() == 0.5
    assert loader.sel_gen.file_id == 2

def test_audio_select_loader_stores_source_data(five_time_stamped_wave_files):
    """ Test that we can use the AudioSelectionLoader class to compute MagSpectrograms
        and that the spectrograms retain the correct source data (filename, offset) """ 
    rep = {'type':'MagSpectrogram','window':0.1,'step':0.02}
    # create a selection table
    files = find_wave_files(path=five_time_stamped_wave_files, return_path=False, search_subdirs=True)
    filename = [files[0],files[1]]
    start = [0.10,0.12]
    end = [0.46,0.42]
    sel = pd.DataFrame({'filename':filename,'start':start,'end':end})
    sel = use_multi_indexing(sel, 'sel_id')
    # init loader
    loader = AudioSelectionLoader(path=five_time_stamped_wave_files, selections=sel, repres=rep)
    assert loader.num() == 2
    for i in range(6): #loop over each item 3 times
        s = next(loader)
        assert s.offset == start[i%2]
        assert s.filename == filename[i%2]

def test_audio_frame_loader_on_2min_wav():
    rep = {'type':'MagSpectrogram', 'window':0.2, 'step':0.02, 'window_func':'hamming', 'freq_max':600.}
    path = os.path.join(path_to_assets, '2min.wav')
    loader = AudioFrameLoader(filename=path, frame=30., step=15., repres=rep)
    assert loader.num() == 8
    s = next(loader)
    assert s.freq_max() == pytest.approx(600, abs=s.freq_res())

def test_audio_frame_loader_subdirs():
    """Test that loader can load audio files from subdirectories"""
    rep = {'type':'MagSpectrogram', 'window':0.2, 'step':0.02, 'window_func':'hamming', 'freq_max':1000.}
    path = os.path.join(path_to_assets, 'wav_files')
    loader = AudioFrameLoader(path=path, frame=30., step=15., repres=rep)
    assert len(loader.sel_gen.files) == 3
    for _ in range(loader.num()):
        _ = next(loader)

def test_audio_select_loader_uniform_duration(five_time_stamped_wave_files):
    """ Test that we can use the AudioSelectionLoader class to compute MagSpectrograms
        with uniform duration by specifying duration in audio representation dictionary """ 
    rep = {'type':'MagSpectrogram','window':0.1,'step':0.02,'duration':0.3}
    # create a selection table
    files = find_wave_files(path=five_time_stamped_wave_files, return_path=False, search_subdirs=True)
    sel = pd.DataFrame({'filename':files})
    sel = use_multi_indexing(sel, 'sel_id')
    # init loader
    loader = AudioSelectionLoader(path=five_time_stamped_wave_files, selections=sel, repres=rep)
    assert loader.num() == 5
    for i in range(5):
        s = next(loader)
        assert s.duration() == rep['duration']

def test_audio_select_loader_entire_files(five_time_stamped_wave_files):
    """ Test that we can use the AudioSelectionLoader class to compute MagSpectrograms
        of entire wav files """ 
    rep = {'type':'MagSpectrogram','window':0.1,'step':0.02}
    # create a selection table
    files = find_wave_files(path=five_time_stamped_wave_files, return_path=False, search_subdirs=True)
    sel = pd.DataFrame({'filename':files})
    sel = use_multi_indexing(sel, 'sel_id')
    # init loader
    loader = AudioSelectionLoader(path=five_time_stamped_wave_files, selections=sel, repres=rep)
    assert loader.num() == 5
    for i in range(5):
        s = next(loader)
        assert s.duration() == 0.5

