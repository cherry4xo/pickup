def parse_ice_candidate(ice_candidate_dict):
    """
    Parses an ICE candidate JSON object and returns an instance of aiortc.RTCIceCandidate.

    :param ice_candidate_json: The ICE candidate JSON object as a string.
    :return: An instance of aiortc.RTCIceCandidate.
    """
    # try:
    #     ice_candidate_dict = json.loads(ice_candidate_json)
    # except json.JSONDecodeError as e:
    #     raise ValueError(f"Invalid JSON: {e}")

    candidate = ice_candidate_dict.get('candidate')
    sdp_mid = ice_candidate_dict.get('sdpMid')
    sdp_mline_index = ice_candidate_dict.get('sdpMLineIndex')
    username_fragment = ice_candidate_dict.get('usernameFragment')

    if not candidate:
        raise ValueError("Missing 'candidate' field in the ICE candidate JSON.")

    data = candidate.split()

    related_address = None
    related_port = None
    tcp_type = None

    if len(data) > 8:
        if data[8].startswith('raddr'):
            related_address = data[9]
            try:
                related_port = int(data[10])
            except ValueError:
                related_port = data[10]
        elif data[8].startswith('tcptype'):
            tcp_type = data[9]

    out = {
        "component": int(data[1]),
        "foundation": data[0],
        "ip": data[4],
        "port": int(data[5]),
        "priority": int(data[3]),
        "protocol": data[2],
        "type": data[7],
        "relatedAddress": related_address,
        "relatedPort": related_port,
        "sdpMid": sdp_mid,
        "sdpMLineIndex": sdp_mline_index,
        "tcpType": tcp_type,
    }

    return out