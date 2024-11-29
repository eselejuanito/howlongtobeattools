/*
Epic Games doesn't allow you to extract your game list directly. With this script, you'll be able to retrieve it. If you want to change the list name from "Backlog" to something like "HowLongToBeat," you can modify it directly in the code.

Important: This script works correctly when you've purchased games individually, whether for free or at a certain price. However, if you've bought multiple games at once, it won't account for them, and you'll need to add them manually. This issue needs to be fixed. It could be improved by using Python to emulate clicks and retrieve the details of each purchase.

You can view your list of purchased games at the following link. Be sure to change the language to English, as HowLongToBeat's database is in that language:
https://www.epicgames.com/account/transactions?lang=en-US&productName=egs
*/

// Function to export data with a custom "|" separator
function exportToCustomFile(data, filename) {
    // Convert data to the desired format
    const fileContent = data.map(row => row.join("|")).join("\n");

    // Create a Blob with the content
    const blob = new Blob([fileContent], { type: "text/plain;charset=utf-8;" });

    // Create a download link
    const link = document.createElement("a");
    const url = URL.createObjectURL(blob);
    link.setAttribute("href", url);
    link.setAttribute("download", filename);

    // Append the link to the DOM, trigger a click, and then remove it
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
}

// Extract data and add additional columns
const tbodies = document.querySelectorAll('tbody');
const data = [];

tbodies.forEach(tbody => {
    const span = tbody.querySelector('td a span span');
    if (span) {
        const title = span.textContent.trim();
        // Add additional columns
        data.push([title, "PC", "Epic Games", "Backlog"]);
    }
});

// Export data to the file
exportToCustomFile(data, "game_list.txt");
