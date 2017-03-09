function [I, plot, p ] = DigitizeMap( filename )
%DigitizeMap Use custom OCR to extract block numbers from map images
%   Detailed explanation goes here
%

% Import and prep
[I, R] = geotiffread(filename);
rotated_I = imrotate(I,-90);
SE = strel('disk',1,0);
% Binarize image
BW = imbinarize(rotated_I);
BW = imcomplement(BW);

% Get regions of interest
s = regionprops(BW, 'BoundingBox');
bb = round(reshape([s.BoundingBox], 4, []).');

%
% Prune initial bounding boxes
%

x_min = 10;
x_max = 40;
y_min = 10;
y_max = 65;

width = bb(:,3);
height = bb(:,4);
idx = (width.*height > 200) & (width > x_min) & (width < x_max) & (height > y_min) & (height < y_max);
bb_out = bb(idx,:);

%figure
%imshow(BW);
%for idx = 1 : length(bb_out)
%    rectangle('Position', bb_out(idx,:), 'edgecolor', 'red','linewidth',2);
%end

%
% Apply some filters maybe?
%

w = bb_out(:,3);
h = bb_out(:,4);
aspectRatio = w./h;

%filterIdx = aspectRatio' < 3;
%bb_out(filterIdx) = [];

%
% Expand bounding boxes
%

bboxes = bb_out;
% Convert from the [x y width height] bounding box format to the [xmin ymin
% xmax ymax] format for convenience.
xmin = bboxes(:,1);
ymin = bboxes(:,2);
xmax = xmin + bboxes(:,3) - 1;
ymax = ymin + bboxes(:,4) - 1;

% Expand the bounding boxes by a small amount.
expansionAmount = 0.0012;
xmin = (1-expansionAmount) * xmin;
ymin = (1-expansionAmount) * ymin;
xmax = (1+expansionAmount) * xmax;
ymax = (1+expansionAmount) * ymax;

% Clip the bounding boxes to be within the image bounds
xmin = max(xmin, 1);
ymin = max(ymin, 1);
xmax = min(xmax, size(BW,2));
ymax = min(ymax, size(BW,1));

% Show the expanded bounding boxes
expandedBBoxes = [xmin ymin xmax-xmin+1 ymax-ymin+1];
%IExpandedBBoxes = insertShape(rotated_I,'Rectangle',expandedBBoxes,'LineWidth',3);

%figure
%imshow(IExpandedBBoxes)
%title('Expanded Bounding Boxes Text')

%
% Merge bounding boxes
%

% Compute the overlap ratio
overlapRatio = bboxOverlapRatio(expandedBBoxes, expandedBBoxes);
%overlapRatio(overlapRatio < 0.5) = 0;

% Set the overlap ratio between a bounding box and itself to zero to
% simplify the graph representation.
n = size(overlapRatio,1);
overlapRatio(1:n+1:n^2) = 0;

% Create the graph
g = graph(overlapRatio);

% Find the connected text regions within the graph
componentIndices = conncomp(g);

% Merge the boxes based on the minimum and maximum dimensions.
xmin = accumarray(componentIndices', xmin, [], @min);
ymin = accumarray(componentIndices', ymin, [], @min);
xmax = accumarray(componentIndices', xmax, [], @max);
ymax = accumarray(componentIndices', ymax, [], @max);

% Compose the merged bounding boxes using the [x y width height] format.
textBB = [xmin ymin xmax-xmin+1 ymax-ymin+1];

%
% Pruning merged bounding boxes
%

y_min = 10;
y_max = 85;

firstColumn = textBB(:,3);
secondColumn = textBB(:,4);
idx = (secondColumn > y_min) & (secondColumn < y_max);
textBBoxes = textBB(idx,:);

%figure
%imshow(BW);
%for idx = 1 : length(textBBoxes)
%    rectangle('Position', textBBoxes(idx,:), 'edgecolor', 'red','linewidth',2);
%end

% Get bounding box locations
text_x = round(textBBoxes(:,1)+textBBoxes(:,3)/2);
text_y = round(textBBoxes(:,2)+textBBoxes(:,4)/2);
textBBoxesLoc = [text_x text_y];

%ITextRegion = insertShape(colorImage, 'Rectangle', textBBoxes,'LineWidth',3);
%figure
%imshow(ITextRegion)
%title('Detected Text')

%
% Perform OCR on numbers (currently custom OCR)
%

ocrtxt = ocr(BW, textBBoxes,'TextLayout','Word','Language','C:\Users\cgraziul\Documents\myLang\tessdata\myLang.traineddata','CharacterSet','0123456789');
%ocrtxt = ocr(BW, textBBoxes,'TextLayout','Word','CharacterSet','0123456789');
t = char(ocrtxt.Text);
t = cellstr(t);
t1 = str2double(t);
m = t1 > 120 | isnan(t1);
t(m) = [];
t = str2double(t);
textBBoxesLoc(m,:) = [];
for_shp = cellstr(num2str(t));

% See what it looks like
%figure
%J1 = insertText(rotated_I,textBBoxesLoc,t,'FontSize',20);
%hold on
%imshow(J1)

% Needs to be transformed to match original image orientation

mean_x = size(I,1)/2;
mean_y = size(I,2)/2;
test = [textBBoxesLoc(:,1)-mean_x+1 textBBoxesLoc(:,2)-mean_y+1];
angle = -pi/2;
rotMat = [cos(angle) sin(angle); -sin(angle) cos(angle)];
rotated = test*rotMat;
plot = round([rotated(:,1)+mean_y+1 rotated(:,2)+mean_x+1]);
%Display text rotates around point (upper left is zero)

%J2 = insertText(I,plot,t,'FontSize',20);
%figure 
%hold on
%imshow(J2)

%
% Convert number locations to lat/long
%

[lat, lon] = intrinsicToGeographic(R,plot(:,1),plot(:,2));

%cell2struct(object,name for field,dimension 2 is column)
%mappoint creates a vector object for writing to shapefile, etc
p = geopoint(lat,lon,cell2struct(for_shp,'block_ocr',2));

end

