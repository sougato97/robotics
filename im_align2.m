
%%%%%%%%%%%%%%%%%%%%%%% Normalized Cross Co-relation %%%%%%%%%%%%%%%%%%%%%%%%

function [final_image,shift] = im_align2(B,G,R)
    
    [new_green,green_shift] = align(B,G);
    [new_red,red_shift] = align(B,R);
    shift(1,:) = green_shift;
    shift(2,:) = red_shift;
    
    clear final_image
    final_image(:,:,1) = new_red;
    final_image(:,:,2) = new_green;
    final_image(:,:,3) = B;
           
end

function [aligned,shift] = align(blue,other)
        
        [blue_row,blue_col] = size(blue);
        delta_row = blue_row*0.3;
        delta_col = blue_col*0.3;

        % we will only take 80% of the image for for comparison 
        % Results in better calculation 
        [other_row,other_col] = size(other);


        % will compare cropped regions  
        % this cropped region is from (50%-30% to 50%+30%) i.e. (20% to 80%)
        cropped_blue = blue(blue_row/2 - delta_row: blue_row/2 + delta_row,  blue_col/2 - delta_col : blue_col/2 + delta_col);
        cropped_blue = double(cropped_blue);
        cropped_other = other(other_row/2 - delta_row: other_row/2 + delta_row,  other_col/2 - delta_col : other_col/2 + delta_col);
        cropped_other = double(cropped_other);

        max = 0;
        for i = -15:15
            for j = -15:15
                % this represents the maximum shift i am using for finding
                % the least ncc 
                shift_other=circshift(cropped_other,[i,j]);
                % this circshift does the job of cross-corelation 
                numerator = sum( sum( cropped_blue .* shift_other )); % this is matrix multiplication and then sum of all its elements 
                blue_sum = sum(sum(double(cropped_blue.^2)));
                other_sum = sum(sum(double(cropped_other.^2)));
                denominator = sqrt(blue_sum * other_sum); % the denominator is used for normalization 
                ncc = numerator/denominator;
                if ncc > max
                    max = ncc;
                    shift_row = i;
                    shift_col = j;
                end
            end
        end
        shift = [shift_row,shift_col];
        aligned = circshift(other,[shift_row,shift_col]);

    end