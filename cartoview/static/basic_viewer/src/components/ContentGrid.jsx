import React, { Component } from 'react'

import { BasicViewerContext } from '../context'
import CartoviewDrawer from './Drawer'
import CartoviewPopup from './Popup'
import { CartoviewSnackBar } from './CommonComponents'
import Grid from '@material-ui/core/Grid'
import IconButton from '@material-ui/core/IconButton'
import MapViewer from './MapViewer'
import MenuIcon from '@material-ui/icons/Menu'
import Paper from '@material-ui/core/Paper'
import PropTypes from 'prop-types'
import Slide from '@material-ui/core/Slide'
import classnames from "classnames"
import compose from 'recompose/compose'
import { withStyles } from '@material-ui/core/styles'
import withWidth from '@material-ui/core/withWidth'

const styles = theme => ({
	root: {
		height: "100%"
	},
	drawer: {
		width: "30%",
		height: "100%",
		zIndex: "1150",
		position: "fixed",
		[theme.breakpoints.down('md')]: {
			width: "90%"
		},
	},
	drawerClose: {
		width: "0%",
		height: "100%",
		zIndex: "1150",
		position: "fixed"
	},
	drawerContentClose: {
		display: 'none'
	},
	drawerContainer: {
		left: "0px !important"
	},
	DrawerBar: {
		width: '28%',
		zIndex: '12',
		display: 'flex',
		flexDirection: 'column',
		position: 'fixed',
		top: '1%',
		[theme.breakpoints.down('md')]: {
			width: "88%",
			top: ".5%"
		},
		left: '1%',
	},
	DrawerOpenBar: {
		width: '97% !important',
		zIndex: '12',
		display: 'flex',
		flexDirection: 'column',
		position: 'absolute',
		top: '1%',
		[theme.breakpoints.down('md')]: {
			top: ".5%"
		},
		left: '1%',
	}
})

function Transition(props) {
	return <Slide direction="left" {...props} />
}
class ContentGrid extends Component {
	render() {
		const { drawerOpen, toggleDrawer } = this.context
		const { classes } = this.props
		return (
			<div className={classes.root}>
				<div className={classnames({ [classes.drawer]: drawerOpen ? true : false, [classes.drawerClose]: drawerOpen ? false : true })}>
					<Paper className={classnames(classes.DrawerBar, { [classes.DrawerOpenBar]: drawerOpen })}>
						<div className="element-flex ">
							<IconButton onClick={toggleDrawer} color="default" aria-label="Open Menu">
								<MenuIcon />
							</IconButton>
							{/* <GeoCodeSearchInput config={this.geoCodingProps()} /> */}
						</div>
						{/* {!childrenProps.geocodeSearchLoading && childrenProps.geocodingResult.length > 0 &&
									<GeoCodeResult
										resetGeocoding={childrenProps.resetGeocoding}
										action={childrenProps.zoomToExtent}
										geocodingResult={childrenProps.geocodingResult}
										geocodeSearchLoading={childrenProps.geocodeSearchLoading}
										boundlessGeoCodingEnabled={childrenProps.config.boundlessGeoCodingEnabled}
									/>} */}
					</Paper>
					<Transition in={drawerOpen} direction={"right"}>
						<CartoviewDrawer className={classnames({ [classes.drawerContentClose]: !drawerOpen })} />
					</Transition>
				</div>
				<Grid className={classes.root} container alignItems={"stretch"} spacing={0}>
					<Grid item xs={12} sm={12} md={12} lg={12} xl={12}>
						<MapViewer />
						<CartoviewPopup />
					</Grid>
				</Grid>
				<CartoviewSnackBar/>
			</div>
		)
	}
}
ContentGrid.contextType = BasicViewerContext
ContentGrid.propTypes = {
	classes: PropTypes.object.isRequired,
	width: PropTypes.string,
}
export default compose(withStyles(styles), withWidth())(ContentGrid)