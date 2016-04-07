--[[
Convert mat files to .th (for spectral-lib)
--]]

matio = require 'matio' -- For loading .mat files
directoryIn = '../Data/Test_mesh_01/samples_mat/'
directoryOut = '../Data/Test_mesh_01/'

-- -- Convert the laplacian
-- -- filename = directory..'1_laplacian'
-- filename = directory..'laplacian' -- Dense matrix
-- x = matio.load(filename..'.mat')
-- torch.save(filename..'.th',{V=x.V})
-- 
-- print('Laplacian ending...')
-- do return end

-- Convert the signals

numFeature = 1000
numSample = 4000
numClass = 8



function alphanumSort(o)
  local function padnum(d) return ("%03d%s"):format(#d, d) end
  table.sort(o, function(a,b)
    return tostring(a):gsub("%d+",padnum) < tostring(b):gsub("%d+",padnum) end)
  return o
end

local p = io.popen('find "'..directoryIn..'" -type f | sort') --Open directory look for files, save data in p. By giving '-type f' as parameter, it returns all files
local i = 1

tensTr = torch.Tensor(numSample, 1, numFeature) -- [nSamples x nChannels x nFeatures]
tensTrLabels = torch.Tensor(numSample)

-- Copy the list of file
filelines = {}
i=1
for file in p:lines() do
    filelines[i] = file:sub(0, file:len() - 4)
    i=i+1
end
print('Sample extracted: '..table.getn(filelines))
filelines = alphanumSort(filelines)

for i, filename in pairs(filelines) do --Loop through all files
    -- Load the file to convert
    print('Loading '..i..': '..filename)
    x = matio.load(filename..'.mat')
    label = math.floor((i-1)*numClass/numSample) -- WORKS ONLY IF SAME NUMBER OF SAMPLE AND FILES ORDERED
    print('Label: '..label)
    
    -- Conversion
    tensTr[i][1] = x.y
    tensTrLabels[i] = label
    
    -- Debug message (to check correctness)
    print('Debug for '..i..':')
    for j=1,10 do
        print(tensTr[i][1][j])
    end
    
    i = i+1
end

print('Try saving the dataset...')
torch.save(directoryOut..'meshData.th',{trdata=tensTr , trlabels=tensTrLabels , tedata=tensTr , telabels=tensTrLabels })
