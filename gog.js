/*
GOG doesn't allow you to extract your game list directly. With this script, you'll be able to retrieve it. If you want to change the list name from "Backlog" to something like "HowLongToBeat," you can modify it directly in the code.

You can view your list of purchased games at the following link:
https://www.gog.com/en/account
*/

// Function to export data with a custom "|" separator
function exportToCustomFile(data, filename) {
    const fileContent = data.map(row => row.join("|")).join("\n");

    const blob = new Blob([fileContent], { type: "text/plain;charset=utf-8;" });

    const link = document.createElement("a");
    const url = URL.createObjectURL(blob);
    link.setAttribute("href", url);
    link.setAttribute("download", filename);

    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
}

const titles = document.querySelectorAll('.product-title__text'); // Usamos el nuevo selector
const data = [];

titles.forEach(titleElement => {
    const title = titleElement.textContent.trim();
    data.push([title, "PC", "GOG", "Backlog"]);
});

exportToCustomFile(data, "game_list.txt");
