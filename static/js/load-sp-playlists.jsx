"use strict";

class PlaylistsToImport extends React.Component {

    constructor(props) {
        super(props);
        this.addPlaylists = this.addPlaylists.bind(this);
        this.toggleCheckbox = this.toggleCheckbox.bind(this);
        this.handlePlaylistsSubmit = this.handlePlaylistsSubmit.bind(this);
        this.createPlaylistCheckbox = this.createPlaylistCheckbox.bind(this);
        this.createCheckboxes = this.createCheckboxes.bind(this);
    }

    // create a set to hold the IDs of the playlists that are selected
    componentWillMount() {
        this.selectedPlaylists = new Set();
    }

    addPlaylists(spPlaylistIds) {
        this.props.addPlaylists(spPlaylistIds);
    }    

    // when a user toggles a checkbox, add or remove the playlist from the set
    toggleCheckbox(spPlaylistId) {
        if (this.selectedPlaylists.has(spPlaylistId)) {
            this.selectedPlaylists.delete(spPlaylistId);
        } else {
            this.selectedPlaylists.add(spPlaylistId);
        }
    }

    // when the form is submitted, prevent default submission,
    // console log the playlists being added,
    // call function to add the playlists to the db
    handlePlaylistsSubmit(evt) {
        evt.preventDefault();
        this.props.addPlaylists(this.selectedPlaylists)    
    }

    createPlaylistCheckbox(spPlaylist) {
        let newCheckbox =
            (<PlaylistCheckbox
                spPlaylistId={spPlaylist.id}
                spPlaylistName={spPlaylist.name}
                handleCheckboxToggle={this.toggleCheckbox}
                key={spPlaylist.id}
            />)
        
        return newCheckbox
    }

    createCheckboxes() {
        return this.props.spPlaylists.map(spPlaylist => this.createPlaylistCheckbox(spPlaylist));
    }

    render() {
        return(
            <div>
                <form onSubmit={this.handlePlaylistsSubmit}>
                    { this.createCheckboxes() }
                    <input type="submit" value="Sync from Spotify"/>
                </form>
            </div>
        )
    }
}


class PlaylistCheckbox extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
        isChecked: false,
        };
        this.changeToggle = this.changeToggle.bind(this);
    }

    changeToggle() {
        this.setState({isChecked: !this.state.isChecked});

        this.props.handleCheckboxToggle(this.props.spPlaylistId);
    }

    render() {
        return (
            <div >
                <input
                    type="checkbox"
                    value={this.props.spPlaylistId}
                    checked={this.state.isChecked}
                    onChange={this.changeToggle}
                />
                {this.props.spPlaylistName}
            </div>
        );
    }
}
