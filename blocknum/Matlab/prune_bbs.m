function bb_out = prune_bbs(bb_in,x_min,x_max,y_min,y_max) 
%bb_out Trims boundary boxes to be within certain width/height tolerances
% boundingBox = [x y width height]
firstColumn = bb_in(:,3);
secondColumn = bb_in(:,4);
idx = (firstColumn.*secondColumn > 200) & (firstColumn > x_min) & (firstColumn < x_max) & (secondColumn > y_min) & (secondColumn < y_max);
bb_out = bb_in(idx,:);
end
