%Read and then concat each of the 6 images.

for i = 1:6
    %Read the image
    temp = imread(['image' num2str(i) '.jpg']); 
    %temp = imread(['image1.jpg']);

    % Get the size (rows and columns) of the image 
    [r,c] = size(temp);
    row_sub=round(r/3); % this is the row size of each glass plate image 
    
    % Code to split the image into three equal parts and store them in B, G, R channels
    B = temp(1:row_sub, 1:c);
    G = temp(row_sub+1:2*row_sub, 1:c);
    R = temp(2*row_sub+1:3*row_sub, 1:c);
    
    % concatenate R,G,B channels and assign the RGB image to ConcatImg variable
    %ConcatImg = cat(3, R, G, B); 
    %imshow(ConcatImg)
    %or we can also use the mentioned below form.
    clear ConcatImg;
    ConcatImg(:,:,1) = R;
    ConcatImg(:,:,2) = G;
    ConcatImg(:,:,3) = B;
    % But I am getting an error while trying out the 2nd way 
    
    % write the image in the form of image1-color.jpg
    imwrite(ConcatImg,['image', num2str(i), '-color.jpg'])
    
    %%%%%%%%%%%%%%%%%%%%%%% Calling the ssd function %%%%%%%%%%%%%%%%%%%%%%%%
    %[blue_row,blue_col] = size(B);
    [ssd_img,shift] = im_align1(B,G,R);
    % write the image in the form of image1-ssd.jpg
    imwrite(ssd_img,['image', num2str(i), '-ssd.jpg'])
    ch = "For image" + num2str(i) + "-ssd.jpg the shift vector is in the order of - " + newline + " GreenY GreenX" + newline + " RedY RedX";
    disp(ch)
    disp(shift)

    %%%%%%%%%%%%%%%%%%%%%%% Calling the ncc function %%%%%%%%%%%%%%%%%%%%%%%%
    %[blue_row,blue_col] = size(B);
    %disp(['disp offsets for image', num2str(i), '.jpg'])
    %ncc_img = im_align2(B,G,R);
    % write the image in the form of image1-ncc.jpg
    %imwrite(ncc_img,['image', num2str(i), 'ncc.jpg'])

    %%%%%%%%%%%%%%%%%%%%%%% Calling the ncc function %%%%%%%%%%%%%%%%%%%%%%%%
    [ncc_img,shift] = im_align2(B,G,R);
    % write the image in the form of image2-ncc.jpg
    imwrite(ncc_img,['image', num2str(i), '-ncc.jpg'])
    ch = "For image" + num2str(i) + "-ncc.jpg the shift vector is in the order of - " + newline + " GreenY GreenX" + newline + " RedY RedX";
    disp(ch)
    disp(shift)

    %%%%%%%%%%%%%%%%%%%%%%% Calling the RANSAC function %%%%%%%%%%%%%%%%%%%%%%%%
    %[ransac_img,shift] = im_align3(B,G,R);
    % write the image in the form of image1-corner.jpg
    %imwrite(ransac_img,['image', num2str(i), '-corner.jpg'])
    %ch = "For image" + num2str(i) + "-corner.jpg the shift vector is in the order of - " + newline + " GreenY GreenX" + newline + " RedY RedX";
    %disp(ch)
    %disp(shift)
    
    %img = imread("image1-color.jpg");
    %harris_img = harris(img);

end





    