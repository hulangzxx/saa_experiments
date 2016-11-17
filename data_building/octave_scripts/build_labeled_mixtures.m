# Author: Valentin Andrei
# E-Mail: am_valentin@yahoo.com

function [m_mixtures, v_labels] = build_labeled_mixtures (v_wavfiles, ...
  n_max_speakers, n_samples_per_count, n_seconds, ...
  fs, frame_ms, frame_inc_ms, n_bits, with_reverb)

  % Usage:
  %
  % This function takes as input a number of wavfiles and creates a set of
  % mixture frames labeled with the number of competing speakers.
  %
  % Input:
  %
  % m_wavfiles          - the array with the name of all the wavfiles
  % n_max_speakers      - the maximum number of speakers per mixture
  % n_samples_per_count - the number of mixtures for each targeted count
  % fs                  - targeted sampling frequency in Hz
  % frame_ms            - the number of milliseconds per frame (multiple of 20 ms)
  % n_bits              - targeted number of bits per sample
  % frame_inc_ms        - the increment per frame in milliseconds
  % n_seconds           - the number of seconds to be analyzed
  % with_reverb         - if 1, enables reverberation inclusion in mixing
  %
  % Output:
  %
  % m_mixtures          - the mixtures, one per row in a matrix_type
  % v_labels            - row vector with corresponding speaker count per mixture
  
  debug = 1;
  
  n_files = length(v_wavfiles);
  n_frame_size = fs / 1000 * frame_ms;
  f_scale = 0.0;
  
  % Size of the dataset. Silence is also accounted for
  
  n_train_test_size = n_samples_per_count * (n_max_speakers + 1);
  
  % Read single speaker filesep
  
  c_speech = {};
  v_n_frames_speech = zeros(n_files, 1);
  c_silence = {};
  v_n_frames_silence = zeros(n_files, 1);
  
  for i = 1 : n_files
  
    [s, start, stop, act] = build_vad_mask(v_wavfiles(i), ...
      fs, frame_ms, n_bits, frame_inc_ms, n_seconds);
      
    [m_speech, n_speech, m_silence, n_silence] = ...
      get_speech_silence_frames(s, start, stop, act);
      
    c_speech{i} = m_speech;
    v_n_frames_speech(i) = n_speech;
    c_silence{i} = m_silence;
    v_n_frames_silence(i) = n_silence;
    
    f_scale_temp = max(s);
    if (f_scale < f_scale_temp)
      f_scale = f_scale_temp;
    end
      
  end
  
  % Build mixtures
  
  m_mixtures = zeros(n_train_test_size, n_frame_size);
  v_labels = zeros(n_train_test_size, 1);
  
  for i = 1 : n_train_test_size

    n_speakers = randi(n_max_speakers + 1) - 1;
    
    if (n_speakers == 0)
    
      n_silence = randi(n_speakers);
      n_frame = randi(size(c_silence{n_silence}, 1));
      
      m_mixtures(i, :) = c_silence{n_silence}(n_frame, :);
      v_labels(i) = 0;
      
    else
      
      v_speakers = get_n_diff_rand(n_speakers, 1, n_max_speakers);
      v_frames = zeros(n_speakers, 1);
      for j = 1 : n_speakers
        v_frames(j) = randi(size(c_speech{j}, 1);
      end
      
      m_single = zeros(n_speakers, n_frame_size);
      for j = 1 : n_speakers
        m_single(j, :) = c_speech{v_speakers(j)}[v_frames(j), :];
      end
      
      if (with_reverb == 0)
        m_mixtures(i, :) = mix_non_reverb(m_single, f_scale);
      else
        % TODO
      end
      
      v_labels(i) = n_speakers;
  
    end
  end
  
  if (debug == 1)
  
    subplot(3, 2, 1); n_test = randi(n_train_test_size); plot(m_mixtures(n_test, :)); grid; xlabel(v_labels(n_test));
    subplot(3, 2, 2); n_test = randi(n_train_test_size); plot(m_mixtures(n_test, :)); grid; xlabel(v_labels(n_test));
    subplot(3, 2, 3); n_test = randi(n_train_test_size); plot(m_mixtures(n_test, :)); grid; xlabel(v_labels(n_test));
    subplot(3, 2, 4); n_test = randi(n_train_test_size); plot(m_mixtures(n_test, :)); grid; xlabel(v_labels(n_test));
    subplot(3, 2, 5); n_test = randi(n_train_test_size); plot(m_mixtures(n_test, :)); grid; xlabel(v_labels(n_test));
    subplot(3, 2, 6); n_test = randi(n_train_test_size); plot(m_mixtures(n_test, :)); grid; xlabel(v_labels(n_test));
  
  end

endfunction
