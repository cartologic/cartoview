import Collapse from '@material-ui/core/Collapse'
import Divider from '@material-ui/core/Divider'
import ExpandMoreIcon from '@material-ui/icons/ExpandMore'
import IconButton from '@material-ui/core/IconButton'
import ListItem from '@material-ui/core/ListItem'
import ListItemIcon from '@material-ui/core/ListItemIcon'
import ListItemSecondaryAction from '@material-ui/core/ListItemSecondaryAction'
import ListItemText from '@material-ui/core/ListItemText'
import PropTypes from 'prop-types'
import React from 'react'
import classnames from 'classnames'
import { withStyles } from '@material-ui/core/styles'

const styles = theme => ({
	expand: {
		transform: 'rotate(0deg)',
		transition: theme.transitions.create('transform', {
			duration: theme.transitions.duration.shortest,
		}),
	},
	expandOpen: {
		transform: 'rotate(180deg)',
	},
})
class Collapsible extends React.Component {
	constructor(props) {
		super(props)
		const { open } = this.props
		this.state = {
			expanded: typeof (open) !== "undefined" ? open : true
		}
	}
	handleDetailsExpand = () => {
		this.setState({ expanded: !this.state.expanded })
	}
	render() {
		const { classes, children, title, icon } = this.props
		return (
			<div>
				<ListItem button onClick={this.handleDetailsExpand}>
					<ListItemIcon>
						{icon}
					</ListItemIcon>
					<ListItemText primary={title} />
					<ListItemSecondaryAction>
						<IconButton
							className={classnames(classes.expand, {
								[classes.expandOpen]: this.state.expanded,
							})}
							onClick={this.handleDetailsExpand}
							aria-expanded={this.state.expanded}
							aria-label="Show more"
						>
							<ExpandMoreIcon />
						</IconButton>
					</ListItemSecondaryAction>
				</ListItem>
				<Collapse in={this.state.expanded} transitionduration="auto" unmountOnExit>
					{children}
					<Divider />
				</Collapse>

			</div>
		)
	}
}
Collapsible.propTypes = {
	classes: PropTypes.object.isRequired,
	title: PropTypes.string.isRequired,
	children: PropTypes.object.isRequired,
	open: PropTypes.bool,
	icon: PropTypes.object.isRequired,
}
export default withStyles(styles)(Collapsible)