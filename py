import ipaddress
import sys


def vlsm(rede, pedidos):
    base = ipaddress.ip_network(rede)
    ini = int(base.network_address)
    fim = int(base.broadcast_address)
    out = []

    # maior primeiro: blocos grandes alinham melhor e sobra menos buraco
    for nome, hosts in sorted(pedidos.items(), key=lambda p: -p[1]):
        bits = (hosts + 1).bit_length()  # menor 2^bits >= hosts + 2
        tam = 1 << bits
        if ini % tam:
            ini += tam - ini % tam
        if ini + tam - 1 > fim:
            raise ValueError(f"sem espaço para {nome}")
        sub = ipaddress.ip_network((ini, 32 - bits))
        out.append((nome, hosts, sub, tam - 2))
        ini += tam
    return out


def main():
    # TODO: ler pedidos de um arquivo/argumentos
    rede = sys.argv[1] if len(sys.argv) > 1 else "192.168.10.0/24"
    pedidos = {"Vendas": 100, "TI": 50, "RH": 25, "Link WAN": 2}

    print(f"{'Setor':<10}{'Pedido':>7}{'Rede':>20}{'Máscara':>17}{'Úteis':>7}")
    for nome, h, sub, uteis in vlsm(rede, pedidos):
        print(f"{nome:<10}{h:>7}{str(sub):>20}{str(sub.netmask):>17}{uteis:>7}")


if __name__ == "__main__":
    main()
