"use strict";

class PlaylistsToImport extends React.Component {

    addPlaylists(evt) {
        this.props.addPlaylists(evt);
    }    
    render() {
        let spPlaylistsToDisplay = [];

        console.log('Spotify playlists:')
        console.log(this.props.sp_playlists)

        for (let sp_playlist of this.props.sp_playlists) {
            spPlaylistsToDisplay.push(<div><input type="checkbox" name="sp_playlists" value={ sp_playlist.id }/>{ sp_playlist.name }</div>);
        }

        console.log(spPlaylistsToDisplay)
        
        return(
            <div>
                <form onSubmit={this.addPlaylists.bind(this)}>
                    { spPlaylistsToDisplay }
                    <input type="submit" value="Sync from Spotify"/>
                </form>
            </div>
        )
    }
}