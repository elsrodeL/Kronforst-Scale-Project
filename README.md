# Kronforst-Scale-Project

## Project Description
Created an Optimized PCA to select features influencing scale color across 8 different families of butterflies and moths including CRISPR-Cas9 mutant variants.

## Aims
Developed a python program to better understand the relationship between butterfly scale morphology and scale color using scraped data from various scientific publications and independent data collected from samples within the lab. Butterflies exhibit a wide range of color diversity. Such color diversity is housed within small structures called scales that cover the wings of lepidopterans. These scales exhibit a huge diversity of sub-structures known as ‘ultra-structures,’ which are associated with each color phenotype. However, it is not well understood if there are any shared morphological traits across scales of the same color when looking at distantly related Lepidoptera species and moths. As such, The Scale Project aims to understand what these shared morphological traits are.  My approach was to develop a method of feature selection using an optimized principal component analysis (PCA) to reduce the dimensionality of our data and select for a set of sub-features that most heavily influenced scale color in the data. I then used this method to analyze different sub-sets of data to extract meaningful analysis and conclusion.

## Applications 
I examined different families of Lepidoptera to find their most important ultra-structure characteristics.Reducing the dimension of the data for all our datasets of different color classifications. Finally, I examine how these features correspond to a color change for a mutant variant of a butterfly in comparison to their wild relatives. 

## Methods

### Color Classification - Color Mapping

I developed a way to apply a variety of color classification methods to these scales by using sampled RGB values to re-label the scale color variable. 
I used a color picker from an image tool and well-known color algorithm to convert the RGB values into their closest definable color according the the CSS3 library. 
These RBG values were used to generate four separate data sets with four unique 'color mappings'. 

Shown below is how the scales from one dataset are mapped to their respective rbg values using a custom 
index of species name, genotype, base scale color, and iridescent scale color. 

```
{'carystoidesescalantei wt white': 'rgb(255,255,255)',
 'papilioxuthus wt cream': 'rgb(248,248,255)',
 'papilioxuthus wt orange': 'rgb(255,165,0)',
 'papilioxuthus wt black': 'rgb(0,0,0)',
 'papilioxuthus wt blue': 'rgb(0,0,255)',
 'papiliopolytes wt white': 'rgb(255,255,255)',
 'graphiumsarpedon wt white': 'rgb(255,255,255)',
 'graphiumsarpedon wt glass + i(glass)': 'rgb(0,255,255)',
 'battusphilenor wt orange': 'rgb(255,165,0)',
 'battusphilenor wt black + i(blue)': 'rgb(0,0,0)',
 'papiliomaackii wt black': 'rgb(0,0,0)',
 'papiliohelenus wt black': 'rgb(0,0,0)',
 'troidesaeacus wt black': 'rgb(0,0,0)',
 'trogonopterabrookiana wt white': 'rgb(255,255,255)',
 'trogonopterabrookiana wt black': 'rgb(0,0,0)'}
```

I then used these mappings of scales to their visible color 
to generate different color labels for those scales and their 
representative color on any visualizations. 

#### Raw Data 

The color is labeled as it is in the publication where we took the data from. 

```
{'white': 'rgb(255,255,255)',
 'cream': 'rgb(248,248,255)',
 'orange': 'rgb(255,165,0)',
 'black': 'rgb(0,0,0)',
 'blue': 'rgb(0,0,255)',
 'glass': 'rgb(0,255,255)',
 'brown': 'rgb(165,42,42)',
 'yellow': 'rgb(255,255,0)',
 'gold': 'rgb(255,215,0)',
 'red': 'rgb(255,0,0)',
 'beige': 'rgb(245,245,220)'}
```

#### Closest Data 

The color is labeled as the closest color to the reference default color values in color.py
given the associated RBG value of the scale. 

```
DEFAULT_COLORS = [
    'white',
    'black',
    'brown',
    'yellow',
    'red',
    'beige',
    'orange',
    'purple',
    'blue',
    'green',
    'grey',
    'lime',
    'ivory',
    'gold'
]
```

Out of the available colors to choose from our color value is re-labeled 
as shown below in the same original dataset as. 

```
{'beige': 'rgb(245,245,220)', 
 'brown': 'rgb(165,42,42)', 
 'black': 'rgb(0,0,0)', 
 'grey': 'rgb(128,128,128)', 
 'white': 'rgb(255,255,255)', 
 'green': 'rgb(0,128,0)', 
 'orange': 'rgb(255,165,0)', 
 'yellow': 'rgb(255,255,0)'}
```

#### RBG Data

The color is labeled to the closest definable color in the CSS3 library. 

```
{'lightgray': 'rgb(211,211,211)',
 'palegoldenrod': 'rgb(238,232,170)',
 'chocolate': 'rgb(210,105,30)', 
 'black': 'rgb(0,0,0)',
 'slategray': 'rgb(112,128,144)',
 'snow': 'rgb(255,250,250)',
 'darkgray': 'rgb(169,169,169)',
 'olivedrab': 'rgb(107,142,35)', 
 'sienna': 'rgb(160,82,45)', 
 'steelblue': 'rgb(70,130,180)', 
 'silver': 'rgb(192,192,192)', 
 'darkslategray': 'rgb(47,79,79)', 
 'cadetblue': 'rgb(95,158,160)', 
 'darkkhaki': 'rgb(189,183,107)', 
 'linen': 'rgb(250,240,230)', 
 'darkorange': 'rgb(255,140,0)', 
 'lightslategray': 'rgb(119,136,153)', 
 'saddlebrown': 'rgb(139,69,19)', 
 'forestgreen': 'rgb(34,139,34)', 
 'firebrick': 'rgb(178,34,34)', 
 'orange': 'rgb(255,165,0)', 
 'burlywood': 'rgb(222,184,135)', 
 'white': 'rgb(255,255,255)', 
 'antiquewhite': 'rgb(250,235,215)', 
 'maroon': 'rgb(128,0,0)', 
 'mintcream': 'rgb(245,255,250)', 
 'greenyellow': 'rgb(173,255,47)', 
 'brown': 'rgb(165,42,42)', 
 'darkolivegreen': 'rgb(85,107,47)', 
 'khaki': 'rgb(240,230,140)', 
 'tan': 'rgb(210,180,140)', 
 'mediumseagreen': 'rgb(60,179,113)', 
 'darkseagreen': 'rgb(143,188,143)'}
```

#### Validate Data

The data is re-labeled in the same fashion as the closest dataset with the exception 
that only data who's original visible scale scale color matches the closest color is included in the 
dataset. It is a way of dropping mis-labeled colors instead of converting the color-name given by the publication’s authors.

Out of 75 individual sources of different scale types drawn form 17 publications only 24 were determined to be correctly classified according to our this method of color validation.
giving us a color mapping of. 

```
{'black': 'rgb(0,0,0)',
 'white': 'rgb(255,255,255)',
 'orange': 'rgb(255,165,0)',
 'brown': 'rgb(165,42,42)',
 'beige': 'rgb(245,245,220)',
 'yellow': 'rgb(255,255,0)'}

```

### PCA for reducing the dimensionality of our data

The paradox when it comes to data is that more is always better, but it can be difficult to extract meaningful information from many variables. 
Because our data is highly dimensional, meaning it has a lot of columns per row, we need a way to extract meaningful insights from our data. 
We use a Principal Component Analysis for this. We take our original seven morphological ultra-scale characteristics and feed them into the method to understand which features are most helpful in resolving data. 
We use a decomposed 2D PCA to easily represent this, however the program can also do 3D PCA’s. 

#### Limitations: 

1. A PCA requires dropping rows where input features are void. Because our data is sourced across many different publications many images were taken without a side-view so the morphological characteristics of 'traburnaculae_length' and 'ridge_elevation' could only be recorded for a small sub-set of the overall data.  Because of this I have conducted multiple PCA’s with different sets of features to choose from which make use of more of the data to construct the PCA. In the rest of this README, I will be referring to two different sets of PCA's one labeled  '2D features' which includes the ultra-structure measurements which only required a top-down image of the scales, which all publications had which was used to generate our data, the other refereed to as '3D features' is a PCA constructed from data generated from pictures that had a side-view image of scales.

2. A PCA is a great way of uncovering ways of differentiating different catagories based on input features. However this categorization based on observable traits is the same process that early naturalist and geneticists adopted to classify the degree of 'relatedness' between species.  Therefore without accounting for the underlying phylogeny of our data or inherent differentiation across species regardless of scale color, we cannot definitively say that the morphological relationships we uncover are the definitive features that define the phenotypic expression of scale color. Instead it is entirely possible that the PCA's we are generating are showing the features which best resolve separate families or more closely related groups. Another way this can happen regardless of the data's underlying phylogeny is that certain colors only appear in certain families or genuses so the morphological distinction with respect to scale color cannot be inferred. 

3. Labels not encoded 

### Feature Selection by Optimizing a PCA for fewer components

## PCA with All Data - Scale Color Classification 
### Using all features vs. 2D features 
### Loaded 2D-PCA : all features
#### Raw Data
#### Closest Data 
#### RBG Data
#### Validate Data

### Loaded 2D-PCA : 2D features (side-view measurements not included)
#### Raw Data
#### Closest Data 
#### RBG Data
#### Validate Data



## Color Analysis by family

## Mutations CRISPR-Cas9

## Executing program

## License

## Acknowledgments
