// ─────────────────────────────────────────────────────────────
//  TCP Handshake site config — edit this file to update the site.
// ─────────────────────────────────────────────────────────────

window.SITE = {
  // Booking requests go here. With no formEndpoint, the form opens
  // the visitor's email app addressed to this address.
  email: "booking@example.com",

  // Optional: a Formspree (or similar) endpoint, e.g.
  // "https://formspree.io/f/abcd1234". When set, the form sends
  // directly from the page instead of opening an email app.
  formEndpoint: "",

  instagram: "", // e.g. "https://instagram.com/tcphandshake"
};

// Parties. Dates are YYYY-MM-DD. Order doesn't matter: upcoming
// shows sort to the top, past ones drop into the log automatically.
// `start` (24h) drives the countdown; `time` is what visitors see.
// `link` is optional (tickets, RSVP). `flyer` names an ASCII flyer in
// flyers/ (made with tools/flyer2ascii.py) shown while it's the next show.
window.EVENTS = [
  {
    date: "2026-10-31",
    start: "19:30",
    time: "7:30PM",
    title: "Halloween Party",
    venue: "DM for address",
    city: "",
    details: ["Costumes required", "Live music & DJ"],
    flyer: "halloween",
    link: "",
  },
];
