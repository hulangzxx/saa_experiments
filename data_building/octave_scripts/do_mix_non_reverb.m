# Author: Valentin Andrei
# E-Mail: am_valentin@yahoo.com

function [s_mixed] = do_mix_non_reverb (m_signals, b_normalize)

  % Usage: mixture = mix_non_reverb(non_mixed);
  %
  % This function mixes more sound signals into one, by adding elements,
  % considering no reverberation effects occur.
  %
  % Input:
  %
  % m_signal  - matrix of input signals, one per rows
  %
  % Output:
  %
  % s_mixed   - mixed signals
  
  debug = 0;

  n_signals = size(m_signals, 1);
  s_mixed = sum(m_signals, 1);
  
  if (b_normalize == 1)
    s_mixed = normalize(s_mixed, 'peak');
  endif

  if (debug == 1)
    subplot(2, 1, 1); plot(m_signals'); grid;
    subplot(2, 1, 2); plot(s_mixed); grid;
  end
  
endfunction