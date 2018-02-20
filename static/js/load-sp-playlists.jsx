"use strict";

class PlaylistsToImport extends React.Component {
    
    render() {
        let spPlaylistsToDisplay = [];

        for (let sp_playlist of this.props.sp_playlists) {
            spPlaylistsToDisplay.push(<input type='checkbox' name='sp_playlists' value={ sp_playlist.id }>{ sp_playlist.name }</br>);
        }
        
        return(
            <form onSubmit=(this.props.addPlaylists)>
                <div className='container'>
                    { spPlaylistsToDisplay }
                    <input type="submit" value="Sync from Spotify">
                </div>
            </form>
        )