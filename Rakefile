# global. files to work with.
files = ['introduction', 'physicists_defn','dimensions','lyapunov_exponents','devaney_defn','on_sensitivity','conjugacy','devaney_vs_wiggins','martelli_defn','li_yorke_defn','marotto_defn']

# strip the original and store it in ./src/
def strip_tex(file)
  orig = File.readlines(file)
  src_name = 'src_' + File.basename(file)
  # pop everything before \begin{document}
  until orig.first.include?('begin{document}')
    orig.delete_at(0)
  end
  # pop it, too
  orig.delete_at(0)
  # take everything before the bibliography
  src = orig.take_while do |line|
    not line.strip.include?('bibliographystyle{')
  end
  
  File.open(File.expand_path(src_name,'./src'), 'w') {|file| file.puts src}
end

# prepare source
task :srcprep do 
  puts "Preparing src texfiles for:"
  files.each do |filename|
    puts "\t- #{filename}"
  end
  files.each do |filename|
    puts "processing #{filename}..."
    texpath = filename + '/' + filename + '.tex'
    strip_tex(File.expand_path(texpath,'./essays'))
  end
  puts "Done."
end

# create main.tex
task :genmain do
  main_tmpl_head = "\\documentclass[11pt,draft]{book}\n\\usepackage{xthesis}\n\\graphicspath{{./images/}}\n\n\\makeindex\n\n"
  
  main_includeonly = "%specify the chapters to be compiled\n\\includeonly{"
  files.each do |name|
    main_includeonly += './src/src_'
    main_includeonly += name 
    main_includeonly += ','
  end
  main_includeonly.gsub!(/,$/,'')
  main_includeonly += "}\n\n"

  main_tmpl_tail = "\n% Bibliography\n\\bibliographystyle{pjgsm}\n\\bibliography{./bibliography/thesis}\n\n% Index\n\\printindex\n\n\\end{document}"

  main_file = 'main.tex'
  puts "Rolling out: #{main_file}."
  File.open(main_file,'w') do |file|
    file.puts main_tmpl_head
    file.puts main_includeonly
    file.puts '\begin{document}' + "\n\n"
    files.each do |name|
      file.puts '\include{./src/src_' + name + "}\n\n"
    end
    file.puts main_tmpl_tail
  end
end

# compile main.pdf by xelatex
task :make do
  system('xelatex main.tex')
  system('bibtex main')
  system('makeindex main')
  system('xelatex main.tex')
  system('xelatex main.tex')
end

# do it all at once
task :all do
  Rake::Task['srcprep'].execute
  Rake::Task['genmain'].execute
  Rake::Task['make'].execute
end

task :clean do
  system('rm main.aux main.log main.dvi main.bbl main.blg main.idx main.ind main.ilg main.toc')
  system('rm src/*.aux')
end
