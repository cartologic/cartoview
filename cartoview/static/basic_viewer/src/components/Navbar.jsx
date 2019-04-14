import AppBar from '@material-ui/core/AppBar'
import PropTypes from 'prop-types'
import React from 'react'
import Toolbar from '@material-ui/core/Toolbar'
import { withStyles } from '@material-ui/core/styles'

const drawerWidth = '100%'
const styles = theme => ({
    root: {
        width: '100%',
    },
    drawerPaper: {
        width: drawerWidth
    },
    drawerHeader: {
        background: theme.palette.primary[500],
        display: 'flex',
        justifyContent: 'flex-end',
        padding: '0 8px',
        ...theme.mixins.toolbar,
    }
})
class NavBar extends React.Component {
    render() {
        const { classes } = this.props
        return (
            <div className={classes.root}>
                <AppBar className={classes.drawerHeader} position="static">
                    <Toolbar>
                    </Toolbar>
                </AppBar>
            </div>
        )
    }
}
NavBar.propTypes = {
    classes: PropTypes.object.isRequired
}
export default withStyles(styles, { withTheme: true })(NavBar)