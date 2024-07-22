clc;clear
% Open the original audio
newData1 = importdata("morning_n_breakfast_original.mp3");

vars = fieldnames(newData1);
for i = 1:length(vars)
    assignin('base', vars{i}, newData1.(vars{i}));
end

% Perform FFT and see which frequencies are available
T = 1/fs;
L = length(data);
t = (0:L-1)*T;
figure
plot(t,data)

figure
Y = fft(data);
P2 = abs(Y/L);
P1 = P2(1:L/2+1);
P1(2:end-1) = 2*P1(2:end-1);
f = fs/L*(0:(L/2));
plot(f,P1) 
title("Single-Sided Amplitude Spectrum of X(t)")
xlabel("f (Hz)")
ylabel("|P1(f)|")

% Selecting 8kHz as carrier wave
fcarrier = 8e3;
fc_sample = fs*7; %7s transmission
Timecarrier = (0:fc_sample-1)*T;
% 350 bits, 7s transmission, so 50 baud or 0.02s per bit
zero_amp = 2e-3;
one_amp = 5e-3;
% The bitmap to be transmitted
bitmap = '01101001 01100011 01110100 01100110 01111011 00110001 01011111 01110011 01101100 00110011 00110011 01110000 01111001 01011111 01001110 01100001 01011001 01110101 01001011 01101001 01011111 01100001 01101100 01100001 01110010 01101101 01011111 00110010 01100001 00110110 00110011 00110100 01100100 01100011 00110001 01100010 01100010 00110010 01111101';
count=1;
for i=1:length(bitmap)
    if(bitmap(i)=='0')
        logicmap(count:count+881) = zero_amp;
    else 
        if(bitmap(i)=='1')
            logicmap(count:count+881) = one_amp;
        else
            logicmap(count:count+881) = 0;
        end
    end
    count=count+882;
end
% Using Amplitude Shift Keying
signal = logicmap.*sin(2*pi*fcarrier*Timecarrier);
% Combine the two signals
new_signal = data;
new_signal(1:length(signal),1) = new_signal(1:length(signal)) + signal;
% New signal
figure
plot(t, new_signal)

figure
Y = fft(new_signal);
P2 = abs(Y/L);
P1 = P2(1:L/2+1);
P1(2:end-1) = 2*P1(2:end-1);
f = fs/L*(0:(L/2));
plot(f,P1) 
title("Single-Sided Amplitude Spectrum of X(t)")
xlabel("f (Hz)")
ylabel("|P1(f)|")

% save the signal
audiowrite("morning_n_breakfast.mp3",new_signal,fs)
