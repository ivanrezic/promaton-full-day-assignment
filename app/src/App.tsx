import axios from "axios";
import { useEffect, useState } from "react";
import "./App.css";

function App() {
  const [meta, setMeta] = useState({
    total_uploads: 0,
    total_downloads: 0,
    total_frames: 0,
    average_width: 0,
    average_height: 0,
  });

  const [downloadUrl, setDownloadUrl] = useState<string | null>(null);

  useEffect(() => {
    const fetchData = async () => {
      try {
        // TODO: adjust to use your API server URL here
        const result = await axios.get("http://localhost:8000/api/meta");
        setMeta(result.data);
      } catch (e) {
        // TODO: This will always fail since we have no server implemented
        setMeta({
          total_uploads: 0,
          total_downloads: 0,
          total_frames: 0,
          average_width: 0,
          average_height: 0,
        });
      }
    };
    fetchData();
  }, []);

  // Upload file to the API and prompt a download
  const handleChange = async (event: any) => {
    const formData = new FormData();
    formData.append("file", event.target.files[0]);
    formData.append("fileName", event.target.files[0].name);
    const config = {
      headers: {
        "content-type": "multipart/form-data",
      },
    };
    // TODO: implement API
    await axios.post("http://localhost:8000/api/upload", formData, config).then((response) => {
      console.log(response)
      setDownloadUrl(response.data.url);
    });
    // // TODO: Return a URL to the user
    // setDownloadUrl("http://localhost:4000/data/qwop");
  };

  return (
    <div className="App">
      <header className="App-header">
        <div>
          {downloadUrl ? (
            <a href={downloadUrl}>Click here to download!</a>
          ) : (
            <form action="/action_page.php">
              <input type="file" onChange={handleChange} />
            </form>
          )}
        </div>
        <div className="container">
          <div className="item">
            <p className="legend">Uploads</p>
            {meta.total_uploads}
          </div>
          <div className="item">
            <p className="legend">Downloads</p>
            {meta.total_downloads}
          </div>
          <div className="item">
            <p className="legend">Total Frames</p>
            {meta.total_frames}
          </div>
          <div className="item">
            <p className="legend">Average Width</p>
            {meta.average_width}px
          </div>
          <div className="item">
            <p className="legend">Average Height</p>
            {meta.average_height}px
          </div>
        </div>
      </header>
    </div>
  );
}

export default App;
