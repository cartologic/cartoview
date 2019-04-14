import IconButton from '@material-ui/core/IconButton'
import Menu from '@material-ui/core/Menu'
import MoreVertIcon from '@material-ui/icons/MoreVert'
import PropTypes from 'prop-types'
import React from 'react'
import { withStyles } from '@material-ui/core/styles'

const ITEM_HEIGHT = 30
export const guidGenerator = () => {
    var S4 = () => {
        return (((1 + Math.random()) * 0x10000) | 0).toString(16).substring(1);
    }
    return (S4() + S4() + "-" + S4() + "-" + S4() + "-" + S4() + "-" + S4() + S4() + S4())
}
const styles = theme => ({
    button: {
        margin: 0,
    }
})
class DropDown extends React.Component {
    constructor(props) {
        super(props)
        this.state = {
            anchorEl: null,
        }
        this.id = guidGenerator()
    }

    handleClick = event => {
        this.setState({ anchorEl: event.currentTarget })
    };

    handleClose = () => {
        this.setState({ anchorEl: null })
    };

    render() {
        const { children, classes } = this.props
        const { anchorEl } = this.state

        return (
            <div>
                <IconButton
                    className={classes.button}
                    aria-label="More"
                    aria-owns={anchorEl ? this.id : null}
                    aria-haspopup="true"
                    onClick={this.handleClick}
                >
                    <MoreVertIcon />
                </IconButton>
                <Menu
                    id={this.id}
                    anchorEl={anchorEl}
                    open={Boolean(anchorEl)}
                    onClose={this.handleClose}
                    PaperProps={{
                        style: {
                            maxHeight: ITEM_HEIGHT * 5,
                            width: 200,
                        },
                    }}
                >
                    {children}
                </Menu>
            </div>
        )
    }
}
DropDown.propTypes = {
    children: PropTypes.any.isRequired,
    classes: PropTypes.object.isRequired,
}
export default withStyles(styles)(DropDown)