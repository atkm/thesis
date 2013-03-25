version = [
'1-2', 
'2-3',
'3-4',
'4-5',
'5-6',
'6-7',
'7-8',
'8-9',
'9-10'
]
#version = ['9-10']
version.each do |v|
  f = 'disk_transformation' + v + '.dat'
  target = 'strip' + v + '.jpg'
  rscript = "dat = read.table('#{f}',header=TRUE); library('ggplot2'); image = ggplot(dat, aes(x = x, y = y)) + geom_point(shape=10, size=0.05,color='darkred'); ggsave(file='#{target}', plot=image)
  "
  command = "echo \" " + rscript + "\" | R --no-save"
  #puts command
  # pipe the command to R noninteractive
  system(command)
end
