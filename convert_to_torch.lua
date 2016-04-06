--[[
Convert mat files to .th (for spectral-lib)
--]]

matio = require 'matio' -- For loading .mat files
directory = '../Data/Test_mesh_01/'

-- -- Convert the laplacian
-- -- filename = directory..'1_laplacian'
-- filename = directory..'laplacian' -- Dense matrix
-- x = matio.load(filename..'.mat')
-- torch.save(filename..'.th',{V=x.V})
-- 
-- print('Laplacian ending...')
-- do return end

-- Convert the signals

numSample = 1000
numClass = 8
    
tensTr = torch.Tensor(numClass,1,numSample) -- [nSamples x nChannels x nFeatures]
tensTrLabels = torch.Tensor(numClass)

for i= 0,numClass-1 do
    
    -- Load the file to convert
    filename = directory..'1_'..i
    x = matio.load(filename..'.mat')
    
    -- Conversion
    tensTr[i+1][1] = x.y
    tensTrLabels[i+1] = i
    
    -- Debug message (to check correctness)
    print('Test for '..i..':')
    for j=1,10 do
        print(tensTr[i+1][1][j])
    end
end

print('Try saving the dataset...')
torch.save(directory..'meshData.th',{trdata=tensTr , trlabels=tensTrLabels , tedata=tensTr , telabels=tensTrLabels })
