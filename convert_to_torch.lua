--[[
Convert mat training and testing files and merge them into a unique .th file (for spectral-lib)
--]]

matio = require 'matio' -- For loading .mat files

-- Parametters

directoryIn = '../Data/Test_mesh_01/samples/'
directoryOut = '../Data/Test_mesh_01/'

numFeature = 1000

-- Utils functions

function alphanumSort(o)
  local function padnum(d) return ("%03d%s"):format(#d, d) end
  table.sort(o, function(a,b)
    return tostring(a):gsub("%d+",padnum) < tostring(b):gsub("%d+",padnum) end)
  return o
end

function stringEndsWith(String, End)
   return End=='' or string.sub(String,-string.len(End))==End
end

function loadListFiles(directoryName)
    -- Load, filter, sort and return the list of the files in the given directory
    
    --Open directory look for files, save data in p. By giving '-type f' as parameter, it returns all files
    local p = io.popen('find "'..directoryName..'" -type f | sort') 
    
    filelines = {}
    i=1
    for file in p:lines() do
        if stringEndsWith(file, '.mat') then -- Filter rights files
            filelines[i] = file:sub(0, file:len() - 4)
            i=i+1
        end
    end
    filelines = alphanumSort(filelines)
    return filelines
end


-- Main Script

function getSamplesTensor(mode)
    if mode == 'Training' then
        listFiles = loadListFiles(directoryIn..'tr/')
        nameMode = 'tr'
    elseif mode == 'Testing' then
        listFiles = loadListFiles(directoryIn..'te/')
        nameMode = 'te'
    end
    
    numSample = table.getn(listFiles)
    
    tensorSamples = torch.Tensor(numSample, 1, numFeature) -- [nSamples x nChannels x nFeatures]
    tensorLabels  = torch.Tensor(numSample)
    
    print(numSample..'  samples for '..mode)
    
    -- Load the samples
    for i, filename in pairs(listFiles) do --Loop through all files
        -- Load the file to convert
        print('Loading '..i..': '..filename)
        x = matio.load(filename..'.mat')
        
        -- Conversion and adding it to the tensor
        tensorSamples[i][1] = x.y
        
        -- Debug message (to check correctness)
        print('Debug for '..i..':')
        for j=1,10 do
            print(tensorSamples[i][1][j])
        end
    end
    
    -- Load the labels
    x = matio.load(directoryIn..nameMode..'labels.mat')
    for i = 1, numSample do
        tensorLabels[i] = x.labels[1][i]
    end
    
    print(tensorLabels:size())
    
    print('Debug labels:')
    for i=1,600 do
        print(tensorLabels[i])
    end
    
    -- Return all
    return tensorSamples, tensorLabels
end

print('----------------------------------------------------')
print('------------------TRAINING------------------------')
print('----------------------------------------------------')
tensTrSamp, tensTrLab = getSamplesTensor('Training')
print('----------------------------------------------------')
print('------------------TESTING-------------------------')
print('----------------------------------------------------')
tensTeSamp, tensTeLab = getSamplesTensor('Testing')

print('Try saving the dataset...')
torch.save(directoryOut..'meshData.th',{trdata=tensTrSamp , trlabels=tensTrLab , tedata=tensTeSamp , telabels=tensTeLab })
