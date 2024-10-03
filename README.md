<body>
    <h1>Duck IMAGE Fetcher</h1>
    <p>Welcome to the <strong>Duck IMAGE Fetcher</strong>! This script fetches images from DuckDuckGo based on the keywords provided in an Excel file, using proxies for anonymous browsing.</p>

  <h2>Features</h2>
    <ul>
        <li>Fetches images from DuckDuckGo based on keywords from an Excel file.</li>
        <li>Supports multithreading for faster image fetching.</li>
        <li>Uses rotating proxies for enhanced anonymity.</li>
        <li>Ability to check and remove dead proxies from a list.</li>
        <li>Customizable number of images to fetch per keyword.</li>
    </ul>

  <h2>Requirements</h2>
    <p>Before running the script, make sure you have the following Python libraries installed:</p>
    <pre>
    pip install pandas requests beautifulsoup4 fake_useragent colorama openpyxl
    </pre>

   <h2>How to Use</h2>
    <ol>
        <li>Prepare two Excel files:
            <ul>
                <li><strong>Keywords file</strong>: Contains keywords in one or more columns. Each row represents a keyword for which images will be fetched.</li>
                <li><strong>Proxies file</strong>: Contains proxy details with columns: IP, Port, Username, and Password. Proxies will be used to make requests.</li>
            </ul>
        </li>
        <li>Run the script and choose whether to provide a custom path to your Excel file or use the default one located in the same directory.</li>
        <li>Image URLs for each keyword will be fetched and saved in an Excel file within an <code>output</code> folder.</li>
        <li>The script supports proxy rotation and multithreading for faster performance.</li>
    </ol>

  <h2>Command Line Interface</h2>
    <p>When running the script, you will be prompted to choose options:</p>
    <ul>
        <li><strong>Option 1:</strong> Enter the path to your Excel file.</li>
        <li><strong>Option 2:</strong> Use the default Excel file (in the same directory).</li>
    </ul>

   <h2>Proxy Management</h2>
    <p>The script includes a feature to check and remove dead proxies. During the process, you will be asked whether you want to remove any dead proxies found.</p>

  <h2>Customization</h2>
    <p>The script allows for customization, including:</p>
    <ul>
        <li>Changing the number of images fetched per keyword (default: 300).</li>
        <li>Adjusting the use of proxies for requests.</li>
        <li>Enabling or disabling multithreading for image fetching.</li>
    </ul>

   <h2>Error Handling</h2>
    <p>If the script encounters any issues fetching images or proxies, it will display appropriate error messages and continue processing the next keyword or proxy.</p>

  <h2>Contributing</h2>
    <p>If you want to contribute to improving this script, feel free to submit a pull request or report any issues.</p>

   <h2>Author</h2>
    <p>Scripted by <strong>@garurprani</strong></p>

   <h2>License</h2>
    <p>This project is licensed under the MIT License.</p>

</body>
