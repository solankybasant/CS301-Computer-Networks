
#include <fstream>
#include "ns3/core-module.h"
#include "ns3/network-module.h"
#include "ns3/internet-module.h"
#include "ns3/point-to-point-module.h"
#include "ns3/applications-module.h"
#include "ns3/stats-module.h"

using namespace ns3;

NS_LOG_COMPONENT_DEFINE ("DemoScriptExample");

// Default Network Topology
//
//       10.1.1.0
// n0 -------------- n1   n2   n3   n4
//    point-to-point  |    |    |    |
//                    ================
//                      LAN 10.1.2.0
// ===========================================================================
//
//         node 0                 node 1
//   +----------------+    +----------------+
//   |    ns-3 TCP    |    |    ns-3 TCP    |
//   +----------------+    +----------------+
//   |    10.1.1.1    |    |    10.1.1.2    |
//   +----------------+    +----------------+
//   | point-to-point |    | point-to-point |
//   +----------------+    +----------------+
//           |                     |
//           +---------------------+
//                5 Mbps, 2 ms


class MyApp : public Application
{
public:
  MyApp ();
  virtual ~MyApp ();

  /**
   * Register this type.
   * \return The TypeId.
   */
  static TypeId GetTypeId (void);
  void Setup (Ptr<Socket> socket, Address address, uint32_t packetSize, uint32_t nPackets, DataRate dataRate);

private:
  virtual void StartApplication (void);
  virtual void StopApplication (void);

  void ScheduleTx (void);
  void SendPacket (void);

  Ptr<Socket>     m_socket;
  Address         m_peer;
  uint32_t        m_packetSize;
  uint32_t        m_nPackets;
  DataRate        m_dataRate;
  EventId         m_sendEvent;
  bool            m_running;
  uint32_t        m_packetsSent;
};

MyApp::MyApp ()
  : m_socket (0),
    m_peer (),
    m_packetSize (0),
    m_nPackets (0),
    m_dataRate (0),
    m_sendEvent (),
    m_running (false),
    m_packetsSent (0)
{
}

MyApp::~MyApp ()
{
  m_socket = 0;
}

/* static */
TypeId MyApp::GetTypeId (void)
{
  static TypeId tid = TypeId ("MyApp")
    .SetParent<Application> ()
    .SetGroupName ("Tutorial")
    .AddConstructor<MyApp> ()
    ;
  return tid;
}

void
MyApp::Setup (Ptr<Socket> socket, Address address, uint32_t packetSize, uint32_t nPackets, DataRate dataRate)
{
  m_socket = socket;
  m_peer = address;
  m_packetSize = packetSize;
  m_nPackets = nPackets;
  m_dataRate = dataRate;
}

void
MyApp::StartApplication (void)
{
  m_running = true;
  m_packetsSent = 0;
  if (InetSocketAddress::IsMatchingType (m_peer))
    {
      m_socket->Bind ();
    }
  else
    {
      m_socket->Bind6 ();
    }
  m_socket->Connect (m_peer);
  SendPacket ();
}

void
MyApp::StopApplication (void)
{
  m_running = false;

  if (m_sendEvent.IsRunning ())
    {
      Simulator::Cancel (m_sendEvent);
    }

  if (m_socket)
    {
      m_socket->Close ();
    }
}

void
MyApp::SendPacket (void)
{
  Ptr<Packet> packet = Create<Packet> (m_packetSize);
  m_socket->Send (packet);

  if (++m_packetsSent < m_nPackets)
    {
      ScheduleTx ();
    }
}

void
MyApp::ScheduleTx (void)
{
  if (m_running)
    {
      Time tNext (Seconds (m_packetSize * 8 / static_cast<double> (m_dataRate.GetBitRate ())));
      m_sendEvent = Simulator::Schedule (tNext, &MyApp::SendPacket, this);
    }
}

static void
CwndChange (Ptr<OutputStreamWrapper> stream, uint32_t oldCwnd, uint32_t newCwnd)
{
  //NS_LOG_UNCOND (Simulator::Now ().GetSeconds () << "\t" << newCwnd);
  *stream->GetStream () << Simulator::Now ().GetSeconds () << "\t" << oldCwnd << "\t" << newCwnd << std::endl;
}



int
main (int argc, char *argv[])
{
  

       

        //TCP variant set to NewReno
        Config::SetDefault("ns3::TcpL4Protocol::SocketType", TypeIdValue (TcpVegas::GetTypeId()));

        NodeContainer nodes;
        nodes.Create (4);


  PointToPointHelper p0p1, p1p2, p2p3;
  p0p1.SetDeviceAttribute("DataRate", StringValue("5Mbps"));
  p0p1.SetChannelAttribute("Delay", StringValue("2ms"));

  p1p2.SetDeviceAttribute("DataRate", StringValue("5Mbps"));
  p1p2.SetChannelAttribute("Delay", StringValue("10ms"));

  p2p3.SetDeviceAttribute("DataRate", StringValue("5Mbps"));
  p2p3.SetChannelAttribute("Delay", StringValue("2ms"));


    // PointToPointHelper p2p;
    // p2p.SetDeviceAttribute("DataRate", StringValue("5Mbps"));
    // p2p.SetChannelAttribute("Delay", StringValue("2ms"));

    NetDeviceContainer devices1 = p0p1.Install(nodes.Get(0), nodes.Get(1));
    NetDeviceContainer devices2 = p1p2.Install(nodes.Get(1), nodes.Get(2));
    NetDeviceContainer devices3 = p2p3.Install(nodes.Get(2), nodes.Get(3));
      //   PointToPointHelper pointToPoint;
      //   pointToPoint.SetDeviceAttribute ("DataRate", StringValue ("5Mbps"));            //set the data rate and delay here
      //   pointToPoint.SetChannelAttribute ("Delay", StringValue ("2ms"));
      // 
      //   NetDeviceContainer devices;
      //   devices = pointToPoint.Install (nodes);





        Ptr<RateErrorModel> em = CreateObject<RateErrorModel> ();  //setting the error model
        em->SetAttribute ("ErrorRate", DoubleValue (0.00001));
        devices3.Get (1)->SetAttribute ("ReceiveErrorModel", PointerValue (em));





        InternetStackHelper stack;
        stack.Install (nodes);

   // Create sub-networks
    Ipv4AddressHelper address;
    address.SetBase("10.1.1.0", "255.255.255.0");
    Ipv4InterfaceContainer interfaces1 = address.Assign(devices1);

    address.SetBase("10.1.2.0", "255.255.255.0");
    Ipv4InterfaceContainer interfaces2 = address.Assign(devices2);

    address.SetBase("10.1.3.0", "255.255.255.0");
    Ipv4InterfaceContainer interfaces3 = address.Assign(devices3);
        // Ipv4AddressHelper address;
        // address.SetBase ("10.1.1.0", "255.255.255.0");
        // Ipv4InterfaceContainer interfaces = address.Assign (devices);

    Ipv4GlobalRoutingHelper::PopulateRoutingTables();


        uint16_t sinkPort = 8080;                                                       // this will be our sink port

        Address sinkAddress = InetSocketAddress (interfaces3.GetAddress (1), sinkPort);
        
  

        PacketSinkHelper packetSinkHelper ("ns3::TcpSocketFactory", InetSocketAddress (Ipv4Address::GetAny (), sinkPort));

        ApplicationContainer sinkApps = packetSinkHelper.Install (nodes.Get (3));             // sinking on node 3


        sinkApps.Start (Seconds (0.));
        sinkApps.Stop (Seconds (20.));





        Ptr<Socket> ns3TcpSocket = Socket::CreateSocket (nodes.Get (0), TcpSocketFactory::GetTypeId ());




        Ptr<MyApp> app = CreateObject<MyApp> ();
        app->Setup (ns3TcpSocket, sinkAddress, 1040, 1000000, DataRate ("100Mbps"));
        nodes.Get (0)->AddApplication (app);
        app->SetStartTime (Seconds (1.));
        app->SetStopTime (Seconds (20.));




        
        AsciiTraceHelper asciiTraceHelper;                                                      //this is for the cwnd
        Ptr<OutputStreamWrapper> stream = asciiTraceHelper.CreateFileStream ("demo.cwnd");
        ns3TcpSocket->TraceConnectWithoutContext ("CongestionWindow", MakeBoundCallback (&CwndChange, stream));



        //detailed trace of queue enq/deq packet tx/rx
        //AsciiTraceHelper ascii;
        //pointToPoint.EnableAsciiAll (ascii.CreateFileStream ("demo-file.tr"));
        p0p1.EnablePcapAll ("demo-file");
        p1p2.EnablePcapAll ("demo-file");
        p2p3.EnablePcapAll ("demo-file");


        



        Simulator::Stop (Seconds (20));
        Simulator::Run ();
        Simulator::Destroy ();

        return 0;




}

