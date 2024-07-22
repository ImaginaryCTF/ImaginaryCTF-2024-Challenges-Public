require 'sinatra'

# Route for the index page
get '/' do
  erb :index
end
