"use strict";

function displayPlaylists(result) {

}

function requestPlaylists(evt) {
    
    let payload = {
        'offset': $(this).attr('data-offset')
    };

    $.get('/more_playlists', payload, displayPlaylists)
}

$("#importMore").on('click', requestPlaylists);


class PlaylistElement extends React.Component {

    constructor(props) {
        super(props);
        this.state = {result: []};
           call method below to add LIST OF FIRST 20 PLAYLISTS to state
        this.getPlaylists = this.getPlaylists.bind(this);
    }

    getPlaylists() {
        let payload = {
            'offset': $(this).attr('data-offset')
        };

        $.get('/more_playlists', payload, displayPlaylists)
    }

    render() {
        return 
    }
}

class FetchPlaylists extends React.Component {

    getPlaylists() {

        let payload = {
            'offset': this.attr('data-offset')
        };

        fetch('/more_playlists.json', payload)
            .then((response) => response.json())
            .then((data) => this.setState({result: this.state.result.concat(data)}
            );
    }

    render() {
        return <span onClick={this.getPlaylists}>
            Load more</span>
    }
}

    
    
    


    render method (on click function, list every item in this.state.result)
}

ReactDOM.render(
    <div>
        <h3>Looks like you haven't added any playlists yet! Sync playlists from Spotify:</h3>
        <form action='/add_playlists' method="POST" id='addPlaylistsForm'>
            {% for sp_playlist in spotify_playlists %}
                <input type="checkbox" name="sp_playlists" value={{ sp_playlist.id }}>
                {{ sp_playlist.name }}</br>
            {% endfor %}
            <input type="submit" value="Sync from Spotify">
        </form>
    </div>,
    document.getElementById("root")
);