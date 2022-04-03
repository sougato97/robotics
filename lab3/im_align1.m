
%%%%%%%%%%%%%%%%%%%%%%% Sum of squared diff %%%%%%%%%%%%%%%%%%%%%%%%

function [final_image,shift] = im_align1(B,G,R)
    
    %B = crop_image(B);
    %G = crop_image(G);
    %R = crop_image(R);
    [new_green,green_shift] = align(B,G);
    [new_red,red_shift] = align(B,R);
    shift(1,:) = green_shift;
    shift(2,:) = red_shift;
    %disp(shift)
    
    clear final_image
    %final_image = cat(3,new_red,new_green,B);
    final_image(:,:,1) = new_red;
    final_image(:,:,2) = new_green;
    final_image(:,:,3) = B;
    %imshow(final_image);
           
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

        MiN = inf;
        for i = -15:15
            for j = -15:15
                % this represents the maximum shift i am using for finding
                % the least ssd 
                shift_other=circshift(cropped_other,[i,j]);
                ssd = sum(sum((double(cropped_blue) - double(shift_other)) .^ 2));
                if ssd < MiN
                    MiN = ssd;
                    shift_row = i;
                    shift_col = j;
                end
            end
        end
        shift = [shift_row,shift_col];
        aligned = circshift(other,[shift_row,shift_col]);

    end