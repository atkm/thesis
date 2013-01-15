# global. files to work with.
files = ['introduction', 'physicists_defn','devaney_defn']

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
    not line.strip.include?('bibliographystyle{plain}')
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


task :genmain do
  main_tmpl_head = "\\documentclass{book}\n\\usepackage{thesis}\n\\graphicspath{{./images/}}\n\n"
  
  main_includeonly = "%specify the chapters to be compiled\n\\includeonly{"
  files.each do |name|
    main_includeonly += './src/src_'
    main_includeonly += name 
    main_includeonly += ','
  end
  main_includeonly.gsub!(/,$/,'')
  main_includeonly += '}'

  main_tmpl_tail = "\n\\bibliographystyle{siam}\n\\bibliography{./bibliography/thesis}\n\\end{document}"

  File.open('main.tex.test','w') do |file|
    file.puts main_tmpl_head
    file.puts main_includeonly
    file.puts '\begin{document}'
    files.each do |name|
      file.puts '\include{./src/src_' + name + '}'
    end
    file.puts main_tmpl_tail
  end
end

task :clean do
  system("rm main.aux main.log main.dvi main.bbl main.blg")
end
