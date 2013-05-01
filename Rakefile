#!/usr/bin/env ruby
# encoding: utf-8
# srcprep; genmain; make; all
# global. files to work with.
files = ['abstract','prelims','logistic','billiards','devaney','li_yorke','symbolic','t-entropy','comparisons']
appendix = ['sarkovskii','ly_thm']
#appendix = ['sarkovskii','other_defns']

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
  appendix.each do |filename|
    puts "\t- #{filename}"
  end
  appendix.each do |filename|
    puts "processing #{filename}..."
    texpath = filename + '/' + filename + '.tex'
    strip_tex(File.expand_path(texpath,'./essays'))
  end
  puts "Done."
end

# create main.tex
task :genmain do
  main_tmpl_head = "\\input{header_main.tex}"
  main_includeonly = "%specify the chapters to be compiled.
  \\includeonly{"
  files.each do |name|
    main_includeonly += './src/src_'
    main_includeonly += name 
    main_includeonly += ','
  end
  main_includeonly.gsub!(/,$/,'')
  main_includeonly += "}\n\n"
  main_begin_document = "\\input{begin_main.tex}"
  main_tmpl_pre_appendix = "%Conclusion. if I need one.
\\chapter*{Conclusion}
\\addcontentsline{toc}{chapter}{Conclusion}
\\chaptermark{Conclusion}
\\markboth{Conclusion}{Conclusion}
%\\input{./src/src_conclusion}

\\appendix"

main_tmpl_post_appendix = "\\backmatter % backmatter makes the index and bibliography appear properly in the t.o.c...

% Bibliography
\\renewcommand{\\bibname}{References}
\\bibliographystyle{bibliography/pjgsm}
\\nocite{*}
\\bibliography{./bibliography/thesis}

% Index
\\printindex

\\end{document}"

main_file = 'main.tex'
puts "Rolling out: #{main_file}."
File.open(main_file,'w') do |file|
  file.puts main_tmpl_head
  file.puts main_includeonly
  file.puts main_begin_document

  files.each do |name|
    unless name == 'abstract' or name == 'introduction' or name == 'conclusion'
      file.puts '\input{./src/src_' + name + "}\n\n"
    end
  end
  file.puts main_tmpl_pre_appendix
  appendix.each do |name|
    file.puts '\input{./src/src_' + name + "}\n\n"
  end
  file.puts main_tmpl_post_appendix
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

# see if it compiles
task :xelatex do
  system('xelatex main.tex')
end

# partially make
task :test do
  Rake::Task['srcprep'].execute
  Rake::Task['genmain'].execute
  Rake::Task['xelatex'].execute
end

# do it all at once
task :all do
  Rake::Task['srcprep'].execute
  Rake::Task['genmain'].execute
  Rake::Task['make'].execute
end

task :clean do
  system('rm main.aux main.log main.dvi main.bbl main.blg main.idx main.ind main.ilg main.toc main.lof main.lot')
  system('rm src/*.aux')
  system('rm src/*.tex')
end
