# Onionprobe

Onionprobe is a tool for testing and monitoring the status of
[Tor Onion Services](https://community.torproject.org/onion-services/).

## Specs

Thanks @irl for the idea and basic specs:

> * [ ] HTTP status codes
> * [ ] Regex for content inside the page
> * [ ] Customisable by test path (not all our sites have content at the root)
> * [ ] Randomisation of timing to avoid systemic errors getting lucky and not
>       detected
> * [ ] Flushing descriptor caches so we're testing as if we're a fresh client
>       (but let's not have to bootstrap every time if we can avoid it)
> * [ ] Page load latency
>
> To get the timings right, the tool should take care of the test frequency and
> just expose the metrics rather than having Prometheus scraping individual
> targets on Prometheus' schedule.

Also thanks hiro for suggestions. Idea initiated during a conversation:

    10:49 +<irl> i wondered if we had something smart that would take a
                 list of onions to check and make sure that you can always fetch descriptors
                 rather than just using cached descriptors etc
    10:49 +<irl> we also need to know about "does the site have useful content?"
    11:00 +<irl> you configure it with a set of onion addresses, and it
                 goes in a loop testing one at a time continuously, each test would wipe out
                 descriptor caches so you're always fetching fresh descriptors and then would
                 fetch a set of paths from each onion. you export
                 prometheus metrics for the connection to the onion service, and extra metrics
                 per path on the status code for each path returned by the server.
    11:01 +<irl> you could add in timing metrics wherever is appropriate
                 there, using the existing blackbox_exporter timing metrics as a model.
    11:01 +<irl> bonus: allow configuring a regex per path for what should
                 be found in the returned content/headers.
    12:23 +<hiro> if you use the prometheus exporter with python one could
                  just use request and beautiful soup to check that the page is returning what
                  one expects
