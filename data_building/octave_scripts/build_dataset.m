# Author: Valentin Andrei
# E-Mail: am_valentin@yahoo.com

addpath ("/home/valentin/Working/phd_project/build_dataset/wavfiles");

wavfiles           = { "/home/valentin/Working/phd_project/build_dataset/wavfiles/S1.wav", ...
                        "/home/valentin/Working/phd_project/build_dataset/wavfiles/S2.wav", ...
                        "/home/valentin/Working/phd_project/build_dataset/wavfiles/S3.wav", ...
                        "/home/valentin/Working/phd_project/build_dataset/wavfiles/S4.wav", ...
                        "/home/valentin/Working/phd_project/build_dataset/wavfiles/S5.wav", ...
                        "/home/valentin/Working/phd_project/build_dataset/wavfiles/S6.wav", ...
                        "/home/valentin/Working/phd_project/build_dataset/wavfiles/S7.wav", ...
                        "/home/valentin/Working/phd_project/build_dataset/wavfiles/S8.wav", ...
                        "/home/valentin/Working/phd_project/build_dataset/wavfiles/S9.wav"};
                        
% wavfiles            = { "/home/valentin/Working/phd_project/build_dataset/wavfiles/TEST.wav", ...
%                        "/home/valentin/Working/phd_project/build_dataset/wavfiles/TEST.wav", ...
%                        "/home/valentin/Working/phd_project/build_dataset/wavfiles/TEST.wav", ...
%                        "/home/valentin/Working/phd_project/build_dataset/wavfiles/TEST.wav", ...
%                        "/home/valentin/Working/phd_project/build_dataset/wavfiles/TEST.wav", ...
%                        "/home/valentin/Working/phd_project/build_dataset/wavfiles/TEST.wav", ...
%                        "/home/valentin/Working/phd_project/build_dataset/wavfiles/TEST.wav", ...
%                        "/home/valentin/Working/phd_project/build_dataset/wavfiles/TEST.wav", ...
%                        "/home/valentin/Working/phd_project/build_dataset/wavfiles/TEST.wav"};                        
                        
fs                  = 44100;
frame_ms            = 200;
frame_inc_ms        = 60;
n_bits              = 16;
n_max_speakers      = 3;
n_samples_per_count = 5000;
n_seconds           = 150;
with_reverb         = 0;

# Collect Features
[m_features, v_labels] = build_labeled_features (wavfiles, ...
  n_max_speakers, n_samples_per_count, n_seconds, ...
  fs, frame_ms, frame_inc_ms, n_bits, with_reverb, 1);
  
# Normalize Features
mu = mean(m_features);
sigma = std(m_features);
m_features_norm = (m_features - mu) ./ sigma;
  
save("-ascii", "x_fft_3_speakers_S1_9_200ms_60_ms_inc_44kHz_5000.txt", "m_features_norm");
save("-ascii", "y_fft_3_speakers_S1_9_200ms_60_ms_inc_44kHz_5000.txt", "v_labels");
