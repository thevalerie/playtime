"use strict";

class CurrentDbPlaylists extends React.Component {

    constructor(props) {
        super(props);
        this.createPlaylistLink = this.createPlaylistLink.bind(this);
        this.createLinks = this.createLinks.bind(this);
    }

    createPlaylistLink(dbPlaylist) {
        let newLink =
            (<PlaylistLink
                dbPlaylistId={dbPlaylist.playlist_id}
                dbPlaylistName={dbPlaylist.name}
                key={dbPlaylist.playlist_id}
            />)
        
        return newLink
    }

    createLinks() {
        console.log(this.props.dbPlaylists)
        return this.props.dbPlaylists.map(dbPlaylist => this.createPlaylistLink(dbPlaylist));
    }

    render() {
        let dbPlaylistsToDisplay

        if (this.props.dbPlaylists.length > 0) {
            dbPlaylistsToDisplay =
                <div>
                    <h3>Select a playlist to work on:</h3>
                    <ul>
                        { this.createLinks() }
                    </ul>
                </div>
        } else {
            dbPlaylistsToDisplay =
                <h3>Looks like you haven't added any playlists yet! Sync playlists from Spotify:</h3>
        }

        return(
            <div>
                { dbPlaylistsToDisplay }
            </div>
        )
    }
}



//         let dbPlaylistsToDisplay = [];
//         let message;

//         console.log('User playlists in db', this.props.playlists)

//         if (this.props.playlists.length > 0) {
//             message = <h3>Select a playlist to work on:</h3>
//             <ul>
//                 { dbPlaylistsToDisplay }
//             </ul>
//         } else {
//             message = <h3>Looks like you haven't added any playlists yet! Sync playlists from Spotify:</h3>
//         }
        
//         return(
//             <div>
//                 { message }
//             </div>
//         )
//     }
// }


class PlaylistLink extends React.Component {
    constructor(props) {
        super(props);
    }

    render() {
        return (
            <div >
                <li>
                    <a href={'/playlist/'+ this.props.dbPlaylistId}>
                    {this.props.dbPlaylistName}
                    </a>
                </li>
            </div>
        );
    }
}