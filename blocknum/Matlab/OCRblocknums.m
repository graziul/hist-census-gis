%
% Script to run OCR on maps and incorporate results into block numbering
% algorithm
%

function OCRblocknums(image_path)

files = dir(char(strcat(image_path,string('*.tif'))));

for f = files'
    [I,plot,p] = DigitizeMap(char(strcat(f.folder,string('\'),f.name)));
    shapewrite(p,char(strcat(f.folder,string('\'),strrep(f.name,'.tif','.shp'))));
end

