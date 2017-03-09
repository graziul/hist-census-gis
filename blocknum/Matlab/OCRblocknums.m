%
% Script to run OCR on maps and incorporate results into block numbering
% algorithm
%

files = dir('C:\Users\cgraziul\Documents\*.tif');

i = 1;
for f = files'
    [I,plot,p] = DigitizeMap(char(strcat(f.folder,string('\'),f.name)));
    shapewrite(p,char(strcat(f.folder,string('\'),string(i),string('.shp'))));
    i = i + 1;
end

