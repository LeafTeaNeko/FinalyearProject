
clear all

t = tcpip('localhost', 50007);
fopen(t);


fwrite(t, 'This is a test message.');



data = fread(t,t.BytesAvailable);
% serverdata='hello server'
% fwrite(t, serverdata);
% read(t, 100)
disp(char(data));



fclose(t);



