AFFIXES_TO_STRIP = ['mount', 'mt', 'mt.', 'peak', 'mountain']


def clean_peak_name(name):
    ''' CascadeClimbers' search is awful and Summitpost's isn't much better.
    To give it the best chance without too many false positives

    detailed rationale/constraints:
    - 'mount stuart' on CascadeClimbers (no quotes) actually returns all "mount"s, so don't do
        that. One solution is to quote the whole thing, but then "argonaut peak" would be too strict
        (since many reports just say "argonaut").
    - Summitpost doesn't care as much about quotes, but it does look for all terms,
        so it's similarly worthwhile to search for "argonaut" instead of "argonaut peak".
    - at the same time, we want multi-word names like "White Chuck" to be respected
    - note that both Summitpost and CascadeClimbers seem to be case insensitive so it's not
        important that we lowercase stuff in here
    '''
    search_name = name.lower()
    for affix in AFFIXES_TO_STRIP:
        chars_to_strip = len(affix) + 1  # Include a space
        if search_name.endswith(' {}'.format(affix)):
            search_name = search_name[:-chars_to_strip]
        if search_name.startswith('{} '.format(affix)):
            search_name = search_name[chars_to_strip:]
    return '"{}"'.format(search_name)
