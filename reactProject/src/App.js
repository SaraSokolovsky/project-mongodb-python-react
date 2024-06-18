import { useState, useEffect } from 'react';
import axios from 'axios';

function MyApi() {
    const [data, setData] = useState('');

    useEffect(() => {
        axios.get('http://127.0.0.1:5000/getPersons')
            .then(response => {
                setData(response.data);
            })
            .catch(error => {
                console.error('There was an error!', error);
            });
    }, []);

    return (
        <div>
            <h1>Data from Python:</h1>
            <pre>{JSON.stringify(data, null, 2)}</pre>
        </div>
    );
}

export default MyApi;