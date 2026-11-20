//  W1163 (P5.11 clause 3) - A PLACE A PERSON CAN GO, AS THE DIRECTORY SAYS IT: the nations it is for, the day the page
//  that says so was read and how, and NOT RECENTLY CHECKED ninety days on. Every word but the joining ones is the
//  server's; nothing is said here about whether a place is open, takes a question or has an appointment.
export type Place = {
  name: string; link: string; for_what: string;
  nations: string[] | null; says_so: string | null; how_read: string | null;
  recently_checked: boolean; checked: string;
};

//  England and Wales; England, Wales and Scotland
const listing = (items: string[]) =>
  (items.length < 2 ? items.join('') : `${items.slice(0, -1).join(', ')} and ${items[items.length - 1]}`);

//  a place with its register row: for whom, when its page was read and how; one with none: said as not checked
export const placeSaid = (p: Place) => (p.nations
  ? `For ${listing(p.nations)}: ${p.checked}${p.how_read ? `, ${p.how_read}` : ''}.`
  : `${p.checked}.`);
