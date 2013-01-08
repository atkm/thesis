#!/usr/bin/ruby

# strip the original and store it in ./src/
def strip_tex(file)
  orig = File.readlines(file)
  src_name = 'src_' + File.basename(file)
  # pop everything before \begin{document}
  until orig[0].strip == '\begin{document}'
    orig.pop
  end
  # pop it, too
  orig.pop
  # take everything before the bibliography
  src = orig.take_while do |line|
    line.strip == '\bibliographystyle{plain}'
  end
  
  File.new(File.expand_path(src_name,'./src'), 'w') do |file|
  file.puts src
  end
end

def tex_compile(files)
  stream = File.read("test.tex")
  system("latex #{stream}")
end

if __FILE__==$0
  files = ['introduction', 'physicists_defn']
  puts "Compiling:"
  files.each do |filename|
    puts filename
  end
  strip_tex(File.expand_path('introduction/introduction.tex','./essays'))
end
