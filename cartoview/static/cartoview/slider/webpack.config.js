var webpack = require( 'webpack' )
var path = require( 'path' )
var BUILD_DIR = path.resolve( __dirname, 'dist' )
var APP_DIR = path.resolve( __dirname, 'src' )
var plugins = [ ]
var filename = '[name].bundle.js'
module.exports = {
    entry: {
        AppSlider: path.join(APP_DIR, 'slider.jsx'),
        AppsList: path.join(APP_DIR, 'AppsList.jsx')
    },
    output: {
        path: BUILD_DIR,
        filename: filename,
        library: '[name]',
        libraryTarget: 'umd',
        umdNamedDefine: true,
        publicPath: "/static/cartoview_geo_collect/dist/"
    },
    node: {
        fs: "empty"
    },
    plugins: [
		new webpack.DefinePlugin( {
            'process.env': {
                'NODE_ENV': JSON.stringify( 'production' )
            }
        } ),
		new webpack.optimize.AggressiveMergingPlugin( ),
		new webpack.optimize.DedupePlugin( ),
		new webpack.NoEmitOnErrorsPlugin( ),
		new webpack.optimize.UglifyJsPlugin( {
            compress: {
                warnings: true
            }
        } )
	],
    resolve: {
        extensions: [ '*', '.js', '.jsx' ]
    },
    module: {
        loaders: [ {
                test: /\.(js|jsx)$/,
                loader: 'babel-loader',
                exclude: /node_modules/
			}, {
                test: /\.xml$/,
                loader: 'raw-loader'
			}, {
                test: /\.json$/,
                loader: "json-loader"
			},
            {
                test: /\.css$/,
                loader: "style-loader!css-loader"
			}, {
			test: /\.(png|jpg|gif)$/,
			loader: 'file-loader'
		}
		],
        noParse: [ /dist\/ol\.js/, /dist\/jspdf.debug\.js/,
            /dist\/js\/tether\.js/ ]
    }
}
