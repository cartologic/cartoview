import { BasicViewerContext } from '../context'
import PropTypes from 'prop-types'
import React from 'react'
import compose from 'recompose/compose'
import { connect } from 'react-redux'
import { withStyles } from '@material-ui/core/styles'
import withWidth from '@material-ui/core/withWidth'

const styles = theme => ({

})
class MapViewer extends React.Component {
	constructor(props) {
		super(props)
	}
	componentDidMount() {
		const { map } = this.context
		map.setTarget(this.mapDiv)
	}
	componentDidUpdate(prevProps, prevState) {
		const { width, reduxMap } = this.props
		const { map, setStateKey } = this.context

		if (prevProps.width !== width) {
			map.updateSize()
		}
	}
	render() {
		return <div id="map" ref={(mapDiv) => this.mapDiv = mapDiv} className="map-panel"></div>
	}
}
MapViewer.contextType = BasicViewerContext
MapViewer.propTypes = {
	classes: PropTypes.object.isRequired,
	width: PropTypes.any.isRequired,
	reduxMap: PropTypes.object.isRequired,
}
const mapStateToProps = (state) => {
	return {
		reduxMap: state.map,
	}
}

const App = connect(mapStateToProps, null)(MapViewer)
export default compose(withStyles(styles), withWidth())(App)