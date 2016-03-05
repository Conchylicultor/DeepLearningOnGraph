clearvars;

% Initialisation
idMesh = '213';
folderName = 'Meshs/';

addpath(genpath('../Tools/gspbox/'));
gsp_start

% Loading the coordinates and crating the graph
coords = load([folderName, idMesh, '_cloud.mat']);
weights = load([folderName, idMesh, '_graph.mat']);

G = gsp_graph(weights.M{1,1});
G.coords = coords.M;

disp(['Plot ', num2str(size(coords.M, 1)), ' vertices'])

% Plotting the graph
param = struct;
%param.show_edges = 1; % Warning: Really slow !!!
gsp_plot_graph(G, param);