# Notes

Different notes about different things that didn't belong anywhere else but didn't need their own category.

	class CSubSystem
	{
	protected:
		HDASS	m_hDass;	// SubSystem handle
		HDEV	m_hDev;		// Driver handle
  ...
  
	class CDout;
	friend class CDOut;

	class CDout : public CSubSystem
	{
	public:
		CDout() : CSubSystem(OLSS_DOUT) {}

		ECODE PutSingleValue (long value, int chan=0, int gain=1) {
						TRACE("DOut: %04x\n",value);
			CHECK_ERROR1(olDaPutSingleValue(m_hDass,value,chan,gain));
		}
	};
