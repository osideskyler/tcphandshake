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
// `link` is optional (tickets, RSVP, flyer).
window.EVENTS = [
  {
    date: "2026-11-14",
    time: "10PM–2AM",
    title: "SAMPLE — Packet Storm",
    venue: "Venue TBA",
    city: "Provo, UT",
    link: "",
  },
  {
    date: "2026-12-05",
    time: "9PM–1AM",
    title: "SAMPLE — Three-Way Handshake",
    venue: "Venue TBA",
    city: "Salt Lake City, UT",
    link: "",
  },
  {
    date: "2026-09-20",
    time: "10PM–2AM",
    title: "SAMPLE — 404 Night",
    venue: "Somewhere",
    city: "Provo, UT",
    link: "",
  },
];
