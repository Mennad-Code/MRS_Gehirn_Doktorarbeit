ii = complex(0,1);

%Referenzwerte für den Kreatin-Haupt- und den NAA-Peak
naa_ref_ppm = 2;
cr_ref_ppm = 3;

%für die Auswahl der entsprechenden Datensätze
dataset_names = {'*135ms_1,5T*','*30ms_1,5T*','*135ms_3T*','*30ms_3T*'};

%Auswahl des entsprechenden Datensatzes
d = 1;

% Lade die FID-Daten aller Spektren
[file_name, file_folder] = get_fname(strcat('Rohdaten Spektren/',dataset_names{d}));
addpath(file_folder);
result = get_fid(file_name);

%Lade Spektrenkorrektur-Parameter und Liste nicht nutzbarer Spektren
[file_name, file_folder] = get_fname(strcat('Parameter/',dataset_names{d}));
addpath(file_folder);
corr_param = readtable(file_name);

%Liste aller Parameter- und Listen-Namen
parameter_namen = corr_param.Properties.VariableNames;

%erzeuge aus allen existierenden Parametern und Listen eine Variable
for i = 1:numel(parameter_namen)
    eval([parameter_namen{i} '=' 'corr_param.(parameter_namen{i});'])
    eval([parameter_namen{i} '=' parameter_namen{i} '(~isnan(' parameter_namen{i} '));'])
end

%Zähler für die tatsächlich verwendeten Spektren
n_selected = 0;

%Array der IDs der tatsächlich verwendeten Spektren
used_id = [];

%verschiedene Eingrenzungen der tatsächlich verwendeten Bereiche des Spektrums
arg_range = [arg_range_min:arg_range_max]; %erste Eingrenzung
overview_range = [overview_range_min:overview_range_max]; %Eingrenzung für eine erste Übersichtsdarstellung
naa_range = [naa_range_min:naa_range_max]; %Referenzbereich des NAA-Peaks

%Chemical-Shift-Skala, wird auf den Kreatin-Haupt- und den NAA-Peak normiert
chemshift_scale = [];

for n = 1:size(result,1)

    %Spektren, die in den Listen für nicht nutzbare Spektren stehen werden nicht verwendet
    if(~any(n==n_unusable) & ~any(n==n_wrong_size) & ~any(n==n_wrong_categ))
        
        fid = [result{n};zeros(1024,1)]; %Zero-Filling zur Verbesserung der Auflösung
        si = size(fid,1); %Größe des fid-Arrays
        n_selected = n_selected+1;
        used_id(n_selected,1) = n;
        
        %die Wirbelstromkorrektur ist nur bei den Spektren, die bei einer Feldstärke von 1,5T aufgenommen worden sind notwendig
        %bei den 3T-Daten ist no_auto_phaco leer, dadurch wird die Korrektur nicht durchgeführt
        if (~any(n==no_auto_phaco) & ~isempty(no_auto_phaco))
          fidw = smooth(fid,41);
          pha = angle(fid);
          phaw = angle(fidw);
          for i = 1:size(fid)
              fid(i) = fid(i)*exp(-ii*phaw(i));
          end
        end

        % vorläufige Fouriertransformation
        y_ft1 = fftshift(fft(fid));
    
        %Referenzbereich für den Kreatin-Haupt-Peak
        range_ref_norm = [ref_norm_begin(n):ref_norm_end(n)];

        %Phasenkorrektur durch empirisch festgestellte Werte
        ft_phase = ft_phase_list(n);

        %Phasenkorrektur
        y_ft1 = y_ft1*exp(-ii*ft_phase*pi/180);
        
        %Eingrenzung auf den sinnvollen Argumentenbereich (gleich für alle
        %Spektren derselben Feldstärke)
        y1 = y_ft1(arg_range);

        % erste nicht kalibrierte Darstellung mit Markierung der Referenzbereiche
        figure(1)
        hold on
            plot(overview_range,real(y1(overview_range))+n_selected*20000,'b')
            plot(range_ref_norm,real(y1(range_ref_norm))+n_selected*20000,'r')
            plot(naa_range,real(y1(naa_range))+n_selected*20000,'k')
            text(overview_range(1),real(y1(overview_range(1)))+n_selected*20000,sprintf('Graph %d',n_selected))
        hold off

        %Bestimmung der Kreatin- und NAA-Peak-Werte, sowie deren Position im Referenzbereich
        [norm_constant,norm_pos_rel] = max(real(y1(range_ref_norm)));
        [naa_peak, naa_pos_rel] = max(real(y1(naa_range)));
        
        %Position der Peak-Werte im gesamten Spektrum
        norm_pos = relativerPunkt(norm_pos_rel,range_ref_norm);
        naa_pos = relativerPunkt(naa_pos_rel,naa_range);

        %Eingrenzungsbereich des am Ende tatsächlich berücksichtigten Spektrums
        %in diesen Bereich fallen alle Punkte bis zu einem gewissen Wert jeweils unter bzw. über der Position des Normierungspunktes
        graph_range = [(norm_pos-graph_range_min):(norm_pos+graph_range_max)];
        
        %bestimme die korrespondierenden Referenzbereiche, sowie die des NAA-Peaks im Eingrenzungsbereiche in graph_range
        range_ref_norm_rel = relativerBereich(range_ref_norm,graph_range);
        naa_range_rel = relativerBereich(naa_range,graph_range);
        naa_pos_gr = relativerBereich(naa_pos,graph_range);
        
        %es wird ein linearer Zusammenhang zwischen dem Index der Peak-Position im Array sowie dem Wert des Chemical-Shifts dieser Position angenommen
        % dadurch gilt: chemical shift = m*index + c, wobei m ein linearer Faktor und c eine Konstante ist
        A = [graph_range_min+1, 1; naa_pos_gr, 1];
        B = [cr_ref_ppm; naa_ref_ppm];
        X = mldivide(A,B);
        m = X(1);
        c = X(2);
        %chemical-shift-werte für alle Spektrenpositionen
        chemshift_scale = ((1:(graph_range_min+graph_range_max+1))*m) + c;

        %erstelle ein normiertes Spektrum
        y_norm = 15000*(y1(graph_range))/norm_constant;

        %erstelle den Array, der alle normierten verwendeten Spektren enthält
        y_group(n_selected,1:size(graph_range,2)) = y_norm;

        %Array der Chemical-Shift-Skalen für alle verwendeten Spektren
        chemshift_scale_group(n_selected,1:size(chemshift_scale,2)) = chemshift_scale;

        %Darstellung der normierten Spektren
        hf = figure(2);
        hold on
            hp = plot(real(y_norm)+n_selected*20000,'b');
            hp2 = plot(range_ref_norm_rel,real(y_norm(range_ref_norm_rel))+n_selected*20000,'r');
            plot(naa_range_rel,real(y_norm(naa_range_rel))+n_selected*20000,'k')
            text(1,y_norm(1)+n_selected*20000,sprintf('Graph %d ID %d',n_selected,n));
        hold off
    
    end
end

%Stelle die verwendeten Spektren noch in einer kachelartigen Anordnung zur besseren Übersichtlichkeit und Beurteilbarkeit dar

num_per_plot = 6;

for i = 1:size(y_group,1)
    y_temp = y_group(i,:);
    chemshift_temp = chemshift_scale_group(i,:);
    if mod(i-1, num_per_plot) == 0
        figure(floor(i/num_per_plot)+3);
        tiledlayout(2, ceil(num_per_plot/2));
        hold on
    end
    
    nexttile;
    hold on
    plot(chemshift_temp,real(y_temp),'b');
    plot(chemshift_temp,imag(y_temp),'g');
    
    ax = gca;
    ax.XMinorTick = true;
    set(ax, 'XDir','reverse')
    
    text(chemshift_temp(1),real(y_temp(1)),sprintf('Graph %d ID %d',i,used_id(i)));
end

%Speichere die Spektren und wichtige Metadaten als Struct in einer MAT-Datei
spektren_struct = struct('IDs',used_id,'Spektren',y_group,'Chemshift',chemshift_scale_group);
suffix = dataset_names{d};
save(['Spektren_',strip(suffix,'*'),'.mat'],'spektren_struct')

%verwendete, benutzerdefinierte Funktionen

%Lade die Rohdaten in eine Variable
function result = get_fid(filename)
    result = load(filename);
    fid_name = fieldnames(result);
    result = result.(fid_name{1});
end

%Lade Dateinamen und Ordnername
function [file_name, file_folder] = get_fname(filepath)
    lis = dir(sprintf(filepath));
    file_name = lis(1).name;
    file_folder = lis(1).folder;
end

% Funktion für das Übersetzen der Normierungsposition auf den gesamten
% Argumentenbereich; kleiner Bereich -> großer Bereich
function norm_pos = relativerPunkt(norm_pos_rel,range)
    norm_pos = norm_pos_rel+range(1)-1;
end

% Funktion für das Übersetzen eines Referenzbereichs oder eines Indexes in einen eingegrenzten
% Referenzbereich; großer Bereich -> kleiner Bereich
function new_range_ref = relativerBereich(range_ref,arg_range)
    new_range_ref = range_ref-arg_range(1)+1;
end