"use strict";

class CurrentDbPlaylists extends React.Component {
    
    render() {
        let dbPlaylistsToDisplay = [];
        let message;

        console.log(this.props.playlists)

        if (this.props.playlists.length > 0) {
            message = <h3>Select a playlist to work on:</h3>
            for (let playlist of this.props.playlists) {
                dbPlaylistsToDisplay.push(<li><a href='/playlist/{ playlist.playlist_id }'>{ playlist.name }</a></li>);
            }
        } else {
            message = <h3>Looks like you haven't added any playlists yet! Sync playlists from Spotify:</h3>
        }
        
        return(
            <div>
                { message }
                <ul>
                    { dbPlaylistsToDisplay }
                </ul>
            </div>
        )
    }
}