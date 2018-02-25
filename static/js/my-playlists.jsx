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

    addPlaylists(spPlaylistIds) {
        // evt.preventDefault();

        // // create an empty FormData object
        // window.formInputs = new FormData();

        // // append the data from the sp-playlists child page
        // window.playlistsToAdd = document.querySelectorAll("input[name='spPlaylists']:checked")
        
        // console.log(playlistsToAdd);

        // for (let playlist of playlistsToAdd) {
        //     console.log(playlist['value']);
        //     formInputs.append('spPlaylists', playlist['value'])
        // }

        // console.log('formInputs', formInputs)

        let spPlaylistIdList = Array.from(spPlaylistIds)
        console.log('playlists:', spPlaylistIdList);

        // create the fetch request
        let fetchOptions = {method: 'post',
                            body: JSON.stringify(spPlaylistIdList),
                            credentials: 'same-origin',
                            headers: {
                                'Accept': 'application/json',
                                'Content-Type': 'application/json'
                                },
                            mode: 'cors'
                            };

        console.log('fetchOptions:', fetchOptions.body)

        fetch('/add_playlists.json', fetchOptions)
            .then((response) => response.json())
            .then((data) => {
                console.log(data);
                console.log(this.state.dbPlaylists);
                // let dbPlaylists = this.state.dbPlaylists;
                // dbPlaylists.push(data)
                this.setState({'dbPlaylists': this.state.dbPlaylists.concat(data)});
            });
    }

    componentWillMount() {
        let fetchOptions = {'method': 'GET', credentials: 'same-origin'};

        fetch('/get_db_playlists.json', fetchOptions) // fetch user's playlists from the db
            .then((response) => response.json())
            .then((data) => {
                console.log('data', data);
                this.setState({'dbPlaylists': this.state.dbPlaylists.concat(data)});
            });
        fetch('/get_sp_playlists.json', fetchOptions)
            .then((response) => response.json())
            .then((data) => {
                this.setState({'spPlaylists': this.state.spPlaylists.concat(data)});
            });
    }

    render() {

        let spPlaylistsDisplay = []

        if (this.state.dbPlaylists.length == 0) {
            spPlaylistsDisplay = <PlaylistsToImport spPlaylists = {this.state.spPlaylists} addPlaylists = {this.addPlaylists} />
        }

        return (
            <div>
                <CurrentDbPlaylists dbPlaylists = {this.state.dbPlaylists} />
                { spPlaylistsDisplay }
            </div>
        )
    }
}

console.log('begin');
ReactDOM.render(
    <UserPlaylists/>,
    document.getElementById('root')
);
console.log('end');

