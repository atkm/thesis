#!/usr/bin/ruby
# orbit.rb
# Compute the orbit of a given function

class Orbit
  attr_reader :result

  def initialize(mapping)
    @mapping = get_mapping(mapping)
    # an array to put results in
    @result = []
  end

  def get_mapping(mapping)
    case mapping
    when 'logistic4'
      lambda{|x| 4*x*(1 - x) }
    when 'logistic2'
      lambda{|x| 2*x*(1 - x) }
    when 'quadratic'
      lambda{|x| x**2 }
    end
  end

  def run(init, step)
    val = init
    @result << val
    (1..step).to_a.each do
      val = @mapping.call(val)
      @result << val
    end
    puts @result.inspect
  end
end

if __FILE__==$0
  abort("need map, init value and step") if ARGV.length != 3
  mapping = ARGV[0]
  init    = ARGV[1].to_f
  step    = ARGV[2].to_i
  orbit = Orbit.new(mapping)
  orbit.run(init, step)
end
