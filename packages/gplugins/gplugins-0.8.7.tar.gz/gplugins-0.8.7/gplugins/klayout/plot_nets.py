import itertools
from pathlib import Path

import klayout.db as kdb
import matplotlib.pyplot as plt
import networkx as nx
from gdsfactory.config import logger

from gplugins.klayout.netlist_spice_reader import NoCommentReader


def _get_subcircuit_name(subcircuit: kdb.SubCircuit) -> str:
    """Get the _cell name_ of a `SubCircuit` instance"""
    return f"{subcircuit.circuit_ref().name}{subcircuit.expanded_name()}"


def netlist_to_networkx(
    netlist: kdb.Netlist,
    fully_connected: bool = False,
    include_labels: bool = True,
    only_most_complex: bool = False,
) -> nx.Graph:
    """Convert a KLayout DB `Netlist` to a networkx graph.

    Args:
        netlist: The KLayout DB `Netlist` to convert to a networkx `Graph`.
        fully_connected: Whether to plot the graph as elements fully connected to all other ones (True) or
            going through other elements (False).
        include_labels: Whether to include labels in the graph connected to corresponding cells.
        only_most_complex: Whether to plot only the circuit with most connections or not.
            Helpful for not plotting subcircuits separately.

    Returns:
        A networkx `Graph` representing the connectivity of the `Netlist`.
    """
    G = nx.Graph()

    top_circuits = list(
        itertools.islice(netlist.each_circuit_top_down(), netlist.top_circuit_count())
    )

    if only_most_complex:
        top_circuits = (max(top_circuits, key=lambda x: x.pin_count()),)

    for circuit in top_circuits:
        # first flatten components that won't be kept
        for subcircuit in circuit.each_subcircuit():
            if subcircuit.name in {"TODO"}:
                circuit.flatten_subcircuit(subcircuit)

        for net in circuit.each_net():
            # Get subcircuit pins if they exist (hierarchical export from KLayout)
            net_pins = [
                _get_subcircuit_name(subcircuit_pin_ref.subcircuit())
                for subcircuit_pin_ref in net.each_subcircuit_pin()
            ]
            # or use all pins (flat like from Cadence SPICE)
            if not net_pins:
                net_pins.extend(pin_ref.pin().name() for pin_ref in net.each_pin())

            # Assumed lone net with only label info
            if (
                include_labels
                and net.expanded_name()
                and "," not in net.expanded_name()
            ):
                G.add_edges_from(zip(net_pins, [net.name] * len(net_pins)))

            if fully_connected:
                G.add_edges_from(itertools.combinations(net_pins, 2))
            else:
                G.add_edges_from(zip(net_pins[:-1], net_pins[1:]))
    return G


def plot_nets(
    filepath: str | Path,
    fully_connected: bool = False,
    interactive: bool = False,
    include_labels: bool = True,
    only_most_complex: bool = False,
) -> None:
    """Plots the connectivity between the components in the KLayout LayoutToNetlist file from :func:`~get_l2n`.

    Args:
        filepath: Path to the KLayout LayoutToNetlist file or a SPICE netlist.
            File extensions should be `.l2n` and `.spice`, respectively.
        fully_connected: Whether to plot the graph as elements fully connected to all other ones (True) or
            going through other elements (False).
        interactive: Whether to plot an interactive graph with `pyvis` or not.
        include_labels: Whether to include labels in the graph connected to corresponding cells.
        only_most_complex: Whether to plot only the circuit with most connections or not.
            Helpful for not plotting subcircuits separately.
    """
    match Path(filepath).suffix:
        case ".l2n" | ".txt":
            l2n = kdb.LayoutToNetlist()
            l2n.read(str(filepath))
            netlist = l2n.netlist()
        case ".spi" | ".spice":
            reader = kdb.NetlistSpiceReader(NoCommentReader())
            netlist = kdb.Netlist()
            netlist.read(str(filepath), reader)
        case _:
            logger.warning("Assuming file is KLayout native LayoutToNetlist file")
            l2n = kdb.LayoutToNetlist()
            l2n.read(str(filepath))
            netlist = l2n.netlist()

    # Creating a graph for the connectivity
    G_connectivity = netlist_to_networkx(
        netlist,
        fully_connected=fully_connected,
        include_labels=include_labels,
        only_most_complex=only_most_complex,
    )

    # Plotting the graph
    if interactive:
        try:
            from pyvis.network import Network
        except ModuleNotFoundError as e:
            raise UserWarning(
                "You need to `pip install pyvis` or `gplugins[klayout]`"
            ) from e

        net = Network(
            select_menu=True,
            filter_menu=True,
        )
        net.show_buttons()
        net.from_nx(G_connectivity)
        net.show("connectivity.html")
    else:
        plt.figure(figsize=(8, 6))
        nx.draw(
            G_connectivity,
            with_labels=True,
            node_size=2000,
            node_color="lightpink",
            font_size=12,
        )
        plt.title("Connectivity")
        plt.show()


if __name__ == "__main__":
    from gdsfactory.samples.demo.lvs import pads_correct, pads_shorted

    from gplugins.common.config import PATH
    from gplugins.klayout.get_netlist import get_l2n

    c = pads_correct()
    c = pads_shorted()
    c.show()

    gdspath = c.write_gds(PATH.extra / "pads.gds")

    l2n = get_l2n(gdspath)
    path = PATH.extra / f"{c.name}.txt"
    l2n.write_l2n(str(path))

    plot_nets(path)
