"use strict";

class UserPlaylists extends React.Component {
    
    constructor(props) {
        super(props);
        this.state = {
            dbPlaylists: [],
            spPlaylists: []
        };
        this.addPlaylists = this.addPlaylists.bind(this);
    }

    addPlaylists(evt) {
        evt.preventDefault();

        // create an empty FormData object
        let formInputs = new FormData();

        // append the data from the sp-playlists child page
        let playlistsToAdd = document.querySelector("input[name='sp_playlists']:checked").value

        formInputs.append('sp_playlists', playlistsToAdd)

        // create the fetch request
        let fetchOptions = {'method': 'POST',
                            'body': formInputs,
                            credentials: 'same-origin'};

        fetch('/add_playlists', fetchOptions)
            .then((response) => response.json())
            .then((data) => {
                this.setState({dbPlaylists: this.state.dbPlaylists.concat(data)});
            });
    }

    componentWillMount() {
        let fetchOptions = {'method': 'GET', credentials: 'same-origin'};

        fetch('/get_db_playlists.json', fetchOptions) // fetch user's playlists from the db
            .then((response) => response.json())
            .then((data) => {
                this.setState({dbPlaylists: this.state.dbPlaylists.concat(data)});
            });
        fetch('/get_sp_playlists.json', fetchOptions)
            .then((response) => response.json())
            .then((data) => {
                this.setState({spPlaylists: this.state.spPlaylists.concat(data)});
            });
    }

    render() {    
        return (
            <div>
                <CurrentDbPlaylists playlists = {this.state.dbPlaylists} />
                <PlaylistsToImport sp_playlists = {this.state.spPlaylists} />
            </div>
        )
    }
}

ReactDOM.render(
    <UserPlaylists>
    <div>CurrentDbPlaylists</div>
    <div>PlaylistsToImport</div>
    </UserPlaylists>,
    document.getElementById('root')
);
