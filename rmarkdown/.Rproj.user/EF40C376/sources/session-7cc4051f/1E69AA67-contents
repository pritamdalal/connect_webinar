library(plumber)
library(tidyverse)

# reading in data from CSV
crop_yields <- read_csv("crop_yields.csv")

#* @apiTitle Crop Yields API
#* @apiDescription Returns crop yield data.

####################
# returns all data #
####################
#* @get /data_all
function(){
  crop_yields
}


###########################################################
# returns crop yield for a give year, product, and entity #
###########################################################
#* @param .year The year of interest (1961 - 2018)
#* @param .product The crop of interest. One of wheat, rice, maize, soybeans, potatoes, beans, peas, cassava, barley, cocoa beans, or bananas.
#* @param .entity The country of interest.
#* @get /crop_yield
function(.year, .product, .entity) {
  filter(crop_yields,
         year == .year,
         product == .product,
         entity == .entity)
}